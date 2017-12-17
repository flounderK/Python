# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 13:38:12 2017

@Author: Clif
"""
#TODO: Separate functions out into seperate importable files, compile regex 
#with re.compile(), Support a text list input for the store numbers & 
#add in functionality to create a brand new excel document from that text
#make the row variable more pythonic

import pandas
import requests
import re
import argparse

def get_retry(url, max_retries=10, *args, **kwargs):
    
    _url = url
    
    _max_retries = max_retries
    retries = 0
    finished = False
    while finished != True:
        try:
            r = requests.get(_url, **kwargs)
            
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

#store_number = '01400433'
def query_store_services(store_number):
    #the website uses angular js
    #here is the url for the data it calls
    url = 'https://www.turkeyhillstores.com/store?store='
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'+
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '+
               'Safari/537.36'}
    r = get_retry(url + store_number, headers=headers)
    services = re.search('(?<=\"storeServices\"\:)\{[^}]+?\}', 
                         str(r.content))[0]
    return services

def convert_to_list(services_string):
    k = re.findall('(?<=")[^"]+(?=":true)', 
                   services_string)
    return k


def main():
    parser = argparse.ArgumentParser(description="Scrape data from " +
                                     "Kroger-owned store chains websites " +
                                     "and return which " + 
                                     "services each store offers")
    parser.add_argument("-f",
                        "--filename",
                        help="Filename in which a list of store " +  
                        "numbers is listed and the services that you " +
                        "wish to track are column names",
                        required=True)
    
    parser.add_argument("-s",
                        "--storeNumberColumn",
                        help="Name of the column that contains " +
                        "store numbers. By default it is set to DIVSTORE",
                        required=False)
    parser.add_argument("-o",
                        "--outputFile",
                        help="Name of the excel document to be outputted. "+
                        "By default, it is set to 'output.xlsx'",
                        required=False)
    parser.add_argument("-inf",
                        "--inputFormat",
                        help="File format that the input file." +
                        "Default is set to __",
                        required=False)
    
    args = parser.parse_args()
    file_name = args.filename
    store_number_column = 'DIVSTORE'
    output = 'output.xlsx'
    
    if args.store_number_column != None:
        store_number_column = args.store_number_column

    if args.output != None:
        output = args.output
        
    #open up excel document, convert to dataframe
    x1 = pandas.ExcelFile(file_name)
    df1 = x1.parse(x1.sheet_names[0])
    column_names = df1.columns
    store_numbers = df1[store_number_column]
    row = 0
    
    for store in store_numbers:
        #services that this store offers
        try:
            store_services = convert_to_list(query_store_services(str(store)))
        except:
            row = row + 1
            continue
        
        #full list of services could be generated as the program executes
        #this will be useful later on
        #for service in store_services:
            #if service not in master_services_list:
                #master_services_list.add(service)
        
        #services that are an exact match to the column names in the document
        matching_services = set(store_services) & set(column_names)  
        
        for service_name in matching_services:
            df1.at[df1.index[row], service_name] = 1
        print(store)
        row = row + 1
        
  
    
    #write dataframe out to new excel document
    writer = pandas.ExcelWriter(output)
    df1.to_excel(writer)
    writer.save()

if __name__ == '__main__':
    main()