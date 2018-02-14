# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:54:37 2017

@author: Cliff.Wolfe
"""
#TODO: rewrite to improve parameter names, fix url_base, and make the regex match oddly written paths
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def get_css(soup, session, url):
    css_links = soup.find_all("link", attrs={"type": "text/css"})
    filename_regex = re.compile("(?<=/)[^/]+$")
    ext_regex = re.compile("\.[^$]{3,4}$")
    for link in css_links:
        if link['href'][0:1] == '//':
            file_location = link['href']
        else:
            file_location = urljoin(url, link['href'])
        r = session.get(file_location)
        if r.status_code == 200:
            extension = re.search(ext_regex, link['href'])
            filename = re.search(filename_regex, link['href'])[0]
            if '?' in filename:
                filename =filename.split('?')[-1]
            if extension == 'None':
                filename = filename + ".css"
            with open(filename, 'wb') as f:
                f.write(r.content)

        link['href'] = filename

#    return css_links

def get_url_base(url):
    #return first part of url, no forward slash at the end
    base = re.match("(\w+://|[^/])[^/]+(?=/)*", url)[0]
    return base



# url = 'http://www.uc.edu'
# s = requests.session()
# r = s.get(url)
# soup = BeautifulSoup(r.content, "lxml")
# get_css(soup=soup, session=s, url=url)
