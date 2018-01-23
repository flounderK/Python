# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:54:37 2017

@author: Cliff.Wolfe
"""
#TODO: rewrite to improve parameter names, fix url_base, and make the regex match oddly written paths
import requests
from bs4 import BeautifulSoup
import re


def get_css(soup, session, url_base):
    
    css_links = soup.find_all("link", attrs={"type": "text/css"})
    i = 0
    for link in css_links:
        
        if link['href'][0] != '/':
            link['href'] = "/" + link['href']

        file_location = url_base + link['href']
        
        r = session.get(file_location)
        if r.status_code == 200:
            new_filename = "css" + str(i) + ".css"
            with open(new_filename, 'wb') as f:
                f.write(r.content) 
        
        link['href'] = new_filename
        i = i+1
   
    return css_links

def get_url_base(url):
    #return first part of url, no forward slash at the end
    base = re.match("(\w+://|[^/])[^/]+(?=/)*", url)[0]
    return base



#url = 'http://srvsp01:8020/configurations.do'
#s = requests.session()
#r = s.get(url)
#soup = BeautifulSoup(r.content, "lxml")
#url_base = get_url_base(url)
#get_css(soup, s, url_base)
