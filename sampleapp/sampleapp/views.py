# -*- coding: utf-8 -*-

import ctypes
import urllib2
import re
import urlparse
from django.http import HttpResponse
from django.template import Context, loader
from bs4 import BeautifulSoup
from urlparse import urljoin

_libso = ctypes.CDLL('/var/www/sampleapp/sampleapp/_foo.so')


BAD_URLS = []
CRAWLLED_URLS = []
REGEX = (
    r'href='        # Match 'href='.
    r"""\""""       # Match quotations.
    r'(.+?)'        # Match one or more characters in a lazy way.
    r"""\""""       # Match quotations.
)
# Add tags to validate.
TAGS = [
    'a',
    'script',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'base',
    'link',
    'form',
    'tr',
    'td',
    'li',
    # TODO(gulati): Look into encoding errors related to select and option tags.
    # 'select',
    # 'option',
    # TODO(gulati): Check for meta tags and other non-visible tags.
    # 'meta',
]
# Regex to check syntax.
# The following regular expression checks for the following

# Good
# <a>
# <a href=”non-html” attribute=”non-html”>
# Bad
# <a href=”non-html attribute=”non-html”>
# <a href=”non-html” attribute=”non-html”
# <a href=”non-html’ attribute=”non-html”>
# <a href=non-html” attribute=”non-html”>
# <a href=’non-html” attribute=”non-html”>
# <a href=”non-html” attribute=”non-html> <script class=”non-html”>
# <a href=”<script>” attribute=”non-html”>

# TODO(gulati): Adapt regular expression and make it generic.
# Does not check for meta tag because there is html content in the tag.
# The regular expression should work for non-html value in double quotes.
# <meta content="some html with tags">
REGEX_SYNTAX = (
    r'<'              # Match '<' at beginning.
    r'/?'             # '/' or nothing.
    r'\w+'            # Match one or more words eg script.
    r'('              # Start group 1.
    r'('              # Start group 2.
    r'\s+'            # One or more spaces.
    r'('              # Start group 3.
    r'.+'             # One or more any character.
    r'\s*'            # Zero or more spaces.
    r'='              # Match '='.
    r'\s*'            # Zero or more spaces.
    r')'              # End group 3.
    r'('              # Start group 4.
    # Check for syntax.
    r'?:'
    r"""\"[^""]*?\""""  # Allow strings with double quotes enclosed.
    r'|'              # Or.
    r"""'[^"']*?'"""  # Allow strings with single quotes enclosed.
    r'|'              # Or.
    r"""[^'">\s]+"""  # Don't allow strings with one single quote
                      # or double quote or >.
    # End check for syntax.
    r')'              # End group 4.
    r'?'              # Match the previous group or nothing.
    r')'              # End group 2.
    r'+'              # One or more occurrences of previous group.
    r'\s*'            # Zero or more spaces.
    r'|'              # Or.
    r'\s*'            # Zero or more spaces.
    r')'              # End group 1.
    r'/?'             # '/' or nothing.
    r'>'              # Close tag.
)

def home(request):
	t = loader.get_template('index.html')
	c = Context({
	    'latest_poll_list': '2',})
	return HttpResponse(t.render(c))

def executeC(request):
	t = loader.get_template('execute.html')
	c_value = _libso.foo()
	c = Context({
	    'c_value': c_value,})
	return HttpResponse(t.render(c))

def GetLinks(soup):
	"""Get all anchor links on page.

	Args:
	  soup: (BeautifulSoup) Soup object containing page source.

	Returns:
	  links: (List) List of all the links on page.
	"""
	links = []
	for a in soup.findAll('a', href=True):
	  search = re.search(REGEX, str(a))
	  if search:
	  	links.append(search.group(1))
	return links

def GetSource(page):
  """Gets page source.

  Args:
    page: (String) URL of the page.

  Returns:
    Page source.
  """
  try:
    url = urllib2.urlopen(page)
    return url.read()
  # pylint: disable=W0703
  # We do not want the script to crash becasue of unforseen 503/400.
  except Exception:
    return ''

def IsAbsolute(url):
  """Checks if a URL is absolute or not.

  Args:
    url: (String) Page URL.

  Returns:
    True/False: True if URL is absolute and false if relative.
  """
  return bool(urlparse.urlparse(url).scheme)


def AbsoluteOrRelative(url_list):
  """Separates absolute from relative URLs.

  Args:
    url_list: (List) List of all URLs.

  Returns:
    [(absolute, relative)]: (List of Tuple) Separated links.
  """
  relative = absolute = []
  for url in url_list:
    if IsAbsolute(url):
      absolute.append(url)
    else:
      relative.append(url)
  return list(set(absolute)), list(set(relative))

def CheckTag(soup, url, tag):
  """Checks tag for HTML error and update BAD_URLS.

  Args:
    soup: (BeautifulSoup) Soup object containing page source.
    url: (String) Page URL.
    tag: (String) Type of tag like anchor or script.
  """
  # Break out if URL is already crawlled.
  if url in CRAWLLED_URLS:
    return

  # Replace http with https.
  # if 'http:' in url:
  #   # Update crawlled URLs.
  #   CRAWLLED_URLS.append(url)
  #   url = url.replace('http:', 'https:')

  # Update crawlled URLs.
  CRAWLLED_URLS.append(url)

  for tag in soup.findAll(tag):
    # Replace '&lt' with '<'.
    # This is to check if '<' or '&lt' is present in the link by mistake.
    tag = str(tag).replace('&lt;', '<')
    tag = tag.split('</')
    tag = tag[0].split('>')
    syntax_check = re.search(REGEX_SYNTAX, tag[0] + '>')

    if len(tag) == 1 or not syntax_check:
      log = {
          'url': url,
          'broken_html': '\"\"\"' + str(tag) + '\"\"\"',
          }
      print url
      # Update list of bad HTML.
      BAD_URLS.append(log)

def Crawl(url, depth=2):
  """Peforms recursive crawlling.

  Args:
    url: (String) URL of the page.
    depth: (integer) Depth from base page.
  """
  if depth < 0:
    return

  # Get all bad URLs.
  content = GetSource(url)

  try:
    soup = BeautifulSoup(content)
  except Exception:
    soup = BeautifulSoup('')

  # Validate tags.
  for tag in TAGS:
    CheckTag(soup, url, tag=tag)

  # Get all anchor links on page.
  links = GetLinks(soup)
  
  # Separate absolute from relative links.
  _, relative = AbsoluteOrRelative(links)

  # Crawl relative links only.
  for relative_url in relative:
    try:
      full_url = urljoin(url, relative_url).encode('utf-8')

      if full_url.endswith('/'):
        full_url = full_url.strip('/')

      # TODO(gulati): Integrate sign-in functionality.
      if full_url not in CRAWLLED_URLS and "heavensgate.com/" in full_url:
        # print full_url
        # Recursive.
        Crawl(full_url, depth=depth-1)
    except Exception, e:
      print '*'*100
      print e
      pass

def brokenURLs(request):
  global BAD_URLS
  global CRAWLLED_URLS
  BAD_URLS = []
  t = loader.get_template('broken_urls.html')
  results = {'results': []}
  url = request.GET.get('url')
  Crawl(url, depth=10)
  results.get('results').append(BAD_URLS)
  return HttpResponse(t.render(Context(results)))