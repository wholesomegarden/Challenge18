import os
import urllib
import io
import gzip
import sys
import urllib.parse
import requests

#import urllib.request
import urllib.request
from urllib.request import Request, urlopen
from pprint import pprint as pp

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

import re

from bs4 import BeautifulSoup
from StringIO import StringIO

def getPage(url):
    req = Request(url)
    #req.add_header('Accept-encoding', 'gzip')
    #headers={'User-Agent': 'Mozilla/5.0'}
    #req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20')
    response = urlopen(req)
    # opener = AppURLopener()
    # response = opener.open(url)
    pp(response)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = response.read()
    return data


soup = None

def didyouMean(q):
    q = str(str.lower(q)).strip()
    url = "http://www.google.com/search?q=" + urllib.parse.quote(q)
    # html = getPage(url)
    page = requests.get(url)
    # if str(page.status_code) == "200":
    soup = BeautifulSoup(page.content, 'html.parser')
    # soup = BeautifulSoup(html)
    return soup
    # ans = soup.find('a', attrs={'class' : 'spell'})
    ans = soup.find('a', _class='gL9Hy')
    print("!!!!!",str(ans))
    try:
        result = repr(ans.contents)
        result = result.replace("u'","")
        result = result.replace("/","")
        result = result.replace("<b>","")
        result = result.replace("<i>","")
        result = re.sub('[^A-Za-z0-9\s]+', '', result)
        result = re.sub(' +',' ',result)
    except AttributeError:
        result = 1
    return result
