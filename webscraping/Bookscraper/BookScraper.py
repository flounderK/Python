# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 08:56:00 2017

@author: Cliff.Wolfe
"""
#TODO: refactor EVERYTHING, implement directory
#structure to reduce overhead caused by wkpdftohtml. Proper Url joining
#function is also needed. Allow original url to be input as argument
#separate the get requests and the Beautiful soup page modifications more
from bs4 import BeautifulSoup
import pdfkit
import requests
import re
import sys, traceback
import glob, os
#import time
from PyPDF2 import PdfFileMerger, PdfFileReader
import argparse
#from PIL import Image

def get_retry(url, session=None, max_retries=10, **kwargs):

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
        
        if r.status_code == 200:
            finished = True
        
        retries = retries + 1
        
        if retries >= _max_retries:
            finished = True
    
    return r


def grabImages(url, session, soup):
    """takes a url, session, and the content of the page and grabs everything
    with an img tag. It writes all of those files to the current directory.
    The function also edits the source file names of the images to match the
    names they are assigned when downloaded."""
    r= session
    #extensions = ['.gif','.jpg','.png']
    count = 0
    for img in soup.find_all("img"):
        imageurl = url + img['src']
        #print(imageurl)
        picture_name = 'p' + str(count) + '.jpg'
        r = get_retry(imageurl, session=session, timeout=5)
        if r.status_code == 200:
            with open(picture_name, 'wb') as f:
                f.write(r.content)
        
        img['src'] = picture_name
        #width, height = Image.open(picture_name).size
        #img['style'] = "width: "+ str(width) +"; height: "+ str(height) + ";"
        
        count = count + 1
    return soup

def grab_page(soup, end_point):
    #Everything** that is important on the webpage is in this tag.
    #**Everything except the CSS apparently
    if soup == end_point:
        return ""
    p = soup.find("div", id="HtmlView")
    p = BeautifulSoup(str(p), "lxml")
    second_soup = '<div class="readerContent htmlreadercontent showhighlights" id="readercontent" style="min-height: 703px; font-size: 24px;">'
    second_soup= BeautifulSoup(second_soup, "lxml")
    if p.body.div == None:
        return None
    
    second_soup.body.div.insert(0, p.body.div)
    #p = p.div.wrap(BeautifulSoup(tag, "lxml"))
    page = BeautifulSoup(str(second_soup), "lxml")
   
    return page

def get_next_page_url(soup, url_base, bookname, end_point):
    #So that we know where to point our next requests.session. 
    #if the tage cant be found it means it is the last page of the book.
    #print(soup)
    url_end = soup.find(class_="navigations navigationsRight")['href'] 

    if url_base + url_end == end_point:
        
        return end_point
    
    #url_end = url_end.split('/')[-1]
    url = url_base + url_end + '?uicode=ohlink'
    return url
#match isbn in url
def get_url_start(url):
    #because rather than have the pictures for each page in the same directory
    #as the page, proquest has them (stored with obfuscated names) 
    #being gathered by a script that is stored in the isbn# directory 
    #so I found that directory in a probably not so great way. 
    r = re.match('(\w){,}://[(\w)(\W)]{,}/(978)*(\d){10}', url)[0]
    return r
    
def strip_inputs(soup):
    #there are three input tags at the end of the document that are not needed
    
    for x in soup.find_all("input"):
        x.replace_with("")
    return soup

def write_to_html(soup):
    #Writing the html to an HTML document, and saving room on your hard drive
    #by rewriting over that document over and over. Yea maybe this could
    #be done better
    file_name = "page.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(str(soup))
    return file_name

def find_bookname(url_start):
    #do something to find the name of the book so it can be passed to 
    #merge_pdfs and cleanup
    isbn = re.search("(?<=/)(978)*(\d){10}$", url_start)[0]
    
    return isbn

def merge_pdfs(bookname):
    # merge every pdf in the current directory
    #find files ending in .pdf - set to filenames
    mtime = lambda f: os.stat(os.path.join(".", f)).st_mtime
    filenames = sorted([f for f in os.listdir(".") if f.endswith('.pdf')],
                        key=mtime)
    
    merger = PdfFileMerger()
    for filename in filenames:
        merger.append(PdfFileReader(filename, 'rb'))
        
    merger.write(bookname + ".pdf")
    merger.close()
    return True

def cleanup(bookname):
    #just match to .pdf, .jpg, and .html and delete all of them except the
    #one named bookname.pdf
    for file in glob.glob("*.pdf"):
        if file != bookname + ".pdf":
            os.remove(file)
    
    for file in glob.glob("*.css"):
        os.remove(file)

    for file in glob.glob("*.html"):
        os.remove(file)
        
    for file in glob.glob("*.jpg"):
        os.remove(file)
        
    return "Directory has been cleaned."

def get_url_base(url):
    base = re.match("(\w){,}://[\.(\w)]{,}/", url)[0] + "/"
    return base

def get_css(soup, session, url_base):
    
    css_links = soup.find_all("link", attrs={"type": "text/css"})
    i = 0
    for link in css_links:
        
        #link['href'] = re.sub("\.\.\/", "", link['href'])
        #if link['href'][0] == '/':
        #    link['href'] = link['href'][1:]
     
        file_location = url_base + link['href']
        #print(file_location)
        r = get_retry(file_location, session=session, timeout=5)
        new_filename = "css" + str(i) + ".css"
        if r.status_code == 200:
            
            with open(new_filename, 'wb') as f:
                f.write(r.content)     
        link['href'] = new_filename
        i = i+1
        
    return css_links

def add_css_tags(soup, link_tags):#figure out how to do this right
    
    for tag in link_tags:    
        soup.body.insert(0, tag)
    
    return soup

def add_meta_tag(soup):
    head = soup.new_tag('head')
    soup.html.insert(0,head)
    tag = BeautifulSoup("<meta content='text/html' charset='utf-8' />", "lxml")
    soup.head.insert(0,tag)
    return soup
#-----------------------------------------------------------------------------------------------------
#Preprocess
#precompiled version of wkhtmltopdf to be added in later
def main():
    parser=argparse.ArgumentParser(description="Scrapes safari books"+
                                   "for textbooks and compiles the html,"+
                                   "Images, and CSS into a PDF of the"+
                                   "textbook")
    
    parser.add_argument("-u",
                        "--url",
                        help="The first page of the textbook on safari books.",
                        required=True)
    
    args = parser.parse_args()
    url=args.url
    
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    options = {'quiet': '',
               'encoding':"UTF-8",
               'page-size':'Letter',
               'dpi':600
               }
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
   
    #url = 'http://proquest.safaribooksonline.com/book/networking/security/9781284055931/appendix-b-alternative-security-terms-and-concepts/23_appendix_b_xhtml?uicode=ohlink'
    count = 1 #this has nothing to do with the while, just the pdf file names
    url_start = get_url_start(url)
    bookname = find_bookname(url_start)
    end_found = False
    url_base = 'http://proquest.safaribooksonline.com'
    end_point = url_start
    #------------------------------------begin Process
    s = requests.session()
    #try:
    print(url_start)
    while (end_found != True):
        
        print("page " + str(count))
    
        r = s.get(url, timeout = 5)
        soup = BeautifulSoup(r.content, "lxml")
        tags_to_add = get_css(soup, s, url_base)
        current_page =  grab_page(soup, end_point) 
        if current_page == None:
            print("Went past book end. Whoops.")
            end_found = True
            break
        
        next_page_url = get_next_page_url(soup, url_base, bookname, end_point)
        print(next_page_url)
        #print(tags_to_add)
        if next_page_url == end_point:
            print("End Found")
            end_found = True
            break
        #css is causing issue with the picture size in pdf output.
        current_page = add_css_tags(current_page, tags_to_add)
        
    
        
        stripped_page = strip_inputs(current_page)
        final_soup = grabImages(url_base,
                                s, stripped_page)
        #This tag fixes utf-8 encoding issues when converted to pdf
        final_soup = add_meta_tag(final_soup)
        filename = write_to_html(final_soup)
        #start doing pdf bullshit
        pdfkit.from_file(filename,
                         'out'+ str(count)+ '.pdf', 
                         configuration=config, 
                         options=options)
        
        count = count + 1
    
        url = next_page_url
        
    s.close()#one session per page. move out of while loop to only have one.
    r.close()   
        #while end
    merge_pdfs(bookname)
    cleanup(bookname)
#except:
    
#    tb = sys.exc_info()[2]
#     tbinfo = traceback.format_tb(tb)[0]
#     pymsg = "PYTHON ERRORS:\nTraceback info:\n" +tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
#     with open("errorlog.log", "a+") as f:
#         f.write(pymsg)
#url = 'http://proquest.safaribooksonline.com/book/networking/security/9781284055931/cover/00_cover_xhtml'

main()