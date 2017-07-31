import bs4 
import json
import requests
import urlparse

def get_url_string():
  """
  Returns the URL under consideration.
  """
  return 'https://www.wearethorn.org/our-work-to-stop-child-sexual-exploitation/'

def get_url_path():
  """
  Return path part of the URL.
  """
  return urlparse.urlparse(get_url_string()).path

def create_beautiful_soup():
  """
  Fetch URL and return BeautifulSoup object.
  """
  page = requests.get(get_url_string(), headers={'User-Agent' : 'Mozilla/5.0'})
  return bs4.BeautifulSoup(page.text, 'lxml')

def is_project_elem(elem):
  """
  Given an element, returns True if it is a project element.
  """
  span_elems = elem.find_all('span')
  for span_elem in span_elems:
    if span_elem.text == 'EXPLORE THE PROJECT':
      return True
  return False

def extract_projects(soup):
  """
  Extracts project elements and returns title and description of the projects.
  """
  elems = soup.find_all(class_='wpb_content_element')
  projects = []
  for elem in elems:
    if is_project_elem(elem):
      projects.append({'title' : elem.h3.text,
                       'description' : elem.p.text})
  return projects

def extract_links(soup):
  """
  Extracts links on the page that don't lead to fragments on the same page.
  """
  elems = soup.find_all('a', href = True)
  # Use a set to remove duplicates
  links_set = set()
  for elem in elems:
    url = elem['href']
    url_parse_result = urlparse.urlparse(url)
    # Include links if they don't reference current page.
    if not ((url_parse_result.path.startswith('/') and
             url_parse_result.path == get_url_path()) or
            url == get_url_string() or url.startswith('#')):
      links_set.add(url)
  return [{'link' : link} for link in links_set]
      

soup = create_beautiful_soup()
links = extract_links(soup)
projects = extract_projects(soup)
output = {'links': links, 'projects': projects}
print json.dumps(output, indent = 4, separators = (',', ': '))
