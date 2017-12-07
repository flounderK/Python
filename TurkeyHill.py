# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 11:50:59 2017

@author: Clif
"""

import requests
import re


#store_number = '01400433'
def query_store_services(store_number):
    #the website uses angular js
    #here is the url for the data it calls
    url = 'https://www.turkeyhillstores.com/store?store='
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'+
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '+
               'Safari/537.36'}
    r = requests.get(url + store_number, headers=headers)
    services = re.search('(?<=\"storeServices\"\:)\{[^}]+?\}', 
                         str(r.content))[0]
    return services
#usage:
#query_store_services('01400433')
def convert_to_list(services_string):
    k = re.findall('(?<=")[^"]+(?=":true)', 
                   query_store_services(services_string))
    return k
#usage:
#convert_to_list(query_store_services('01400433'))
