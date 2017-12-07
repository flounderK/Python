# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 22:51:35 2017

@author: Clif
"""

search_expressions = {"file_extension":"\.\w{3,4}$", 
                      "file_name":"(?<=/)[^/]+$",
                      "MAC_addr":"([a-fA-F0-9]{2}[:-]*){6}"}

match_expressions = {"url_base":"(\w+://|[^/])[^/]+(?=/)*"}