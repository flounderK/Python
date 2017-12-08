# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:17:59 2017

@author: Cliff.Wolfe
"""

import requests
from bs4 import BeautifulSoup

url = 'https://www.turkeyhillstores.com/storeHours'

s = requests.session()

def get_retry(session, url, max_retries, *args, **kwargs):
    
    _url = url
    s = session
    _max_retries = max_retries
    retries = 0
    finished = False
    while finished != True:
        try:
            r = s.get(_url, **kwargs)
            
        except requests.ConnectionError as e: 
            print("No response")
            r = requests.Response
            r.status_code = 0
        except requests.exceptions.ReadTimeout as e:
            print("Timeout")
            r = requests.Response
            r.status_code = 0
            
        if r.status_code == 200:
            finished = True
        
        retries = retries + 1
        
        if retries >= _max_retries:
            finished = True
    
    return r

get_retry(s, url, 2)
get_retry(s, url, 2, timeout=5)
