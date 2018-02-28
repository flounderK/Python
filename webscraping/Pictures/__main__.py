# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:20:49 2017

@author: Clif
"""
#TODO: Allow user to specify where images are downloaded to, Determine if urllib.parse.urljoin is more efficient than 
#url joining if statements at line 60
from bs4 import BeautifulSoup
import requests
import re
import argparse
import os

def get_retry(url, max_retries=10, session=None, **kwargs):
    """requests.get but it retries the request a specified number of times"""
    _url = url
    _max_retries = max_retries
    if session != None:
        s=session
    else:
        s=requests.session()
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
        #raise an error here

        if r.status_code == 200:
            finished = True

        retries = retries + 1

        if retries >= _max_retries:
            finished = True

    return r


#start of function
def download_images(url, session, soup, path=None, default_filetype='.jpg', **kwargs):
    """Finds all img tags on a website and downloads the pictures"""
    #regex compiled ahead of time
    base_url_regex = re.compile("(\w+://|[^/])[^/]+")
    img_name_regex = re.compile("(?<=/)[^/]+$")
    ext_regex = re.compile("\.\w{3,4}$")
    name_list = list()
    if not path:
        file_path = "./pics"
    else:
        file_path = path
    
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    for img in soup.find_all("img"):

        #get_url_base makes sure that there is no forward slash at the end
        url_base = re.match(base_url_regex, url)[0]

        #making sure that we get the url for the image correct
        if img['src'][0] == '/':
            imageurl = url_base + img['src']
        elif img['src'][0] == '.':
            imageurl = url_base + '/' + img['src']
        else:
            imageurl = img['src']

        #getting image name
        image_name = re.search(img_name_regex, img['src'])[0]
        if '?' in image_name:
            image_name = image_name.split('?')[0]

        #Here the match of the regex search does not need to be selected
        #because we only care if it is missing
        extension = re.search(ext_regex, image_name)
        if extension == 'None':
            #Image is most likely being called with a script,
            #default to a different filetype
            image_name = image_name + default_filetype
        r = get_retry(session=session, url=imageurl, timeout = 5, **kwargs)
        if r.status_code == 200:
            with open(image_name, 'wb') as f:
                f.write(r.content)
        else:
            return r.status_code

        name_list.append(image_name)

    print("Images downloaded:")
    for name in name_list:
        print name


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",
                        "--url",
                        help="The url you would like to scrape",
                        required=True)
    parser.add_argument("-p",
                        "--path",
                        help="The path to output images to",
                        required=False)
    args = parser.parse_args()

    url = args.url
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'+
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '+
               'Safari/537.36'}
    download_images(url=url, session=s, soup=soup, headers=headers)
