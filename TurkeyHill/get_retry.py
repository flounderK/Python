
import requests

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
