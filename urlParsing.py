import re

def get_url_base(url):
    #return first part of url, no forward slash at the end
    base = re.match("(\w+://|[^/])[^/]+(?=/)*", url)[0]
    return base
