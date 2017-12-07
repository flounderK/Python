# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:20:49 2017

@author: Clif
"""
from bs4 import BeautifulSoup
import requests
import re

def get_url_base(url):
    #return first part of url, no forward slash at the end
    base = re.match("(\w+://|[^/])[^/]+(?=/)*", url)[0]
    return base

#start of function
def download_images(url, session, soup, default_filetype='.jpg'):
    _soup = soup
    _url = url
    _session = session
    for img in _soup.find_all("img"):
        
        #get_url_base makes sure that there is no forward slash at the end
        url_base = get_url_base(_url)
        
        #making sure that we get the url for the image correct
        if img['src'][0] == '/':    
            imageurl = url_base + img['src']
        elif img['src'][0] == '.':
            imageurl = url_base + '/' + img['src']
        else:
            imageurl = img['src']
                
        #getting image name
        image_name = re.search("(?<=/)[^/]+$", img['src'])[0]
        extension = re.search("\.\w{3,4}$", image_name)
        if extension == 'None':
            #"Image is being called with a script," +
            #" naming image after token and defaulting to jpg"
            image_name = image_name + default_filetype
        
        #this next chunk can be removed after error function is tested and used
        r = _session.get(imageurl, timeout = 5)
        if r.status_code == 200:
            with open(image_name, 'wb') as f:
                f.write(r.content)
        
        img['src'] = image_name
    return soup

#usage:            
#url = 'https://pixabay.com/'
#s = requests.session()
#r = s.get(url)
#soup = BeautifulSoup(r.content, "lxml")
#download_images(url, s, soup)
            
            
            
            
            
            
            
            
            
            
            
