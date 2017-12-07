# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 11:50:59 2017

@author: Clif
"""

import requests
import re


store_number = '01400433'
#the website uses angular js
#here is the url for the data it calls
url = 'https://www.turkeyhillstores.com/store?store='
s = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'+
           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '+
           'Safari/537.36'}
#original page url
#url = 'https://www.turkeyhillstores.com/storeHours?store=01400433'
r = s.get(url + store_number, headers=headers)
k = re.search('\"storeServices\"\:\{[\W\w]+?\}', str(r.content))
print(k[0])
