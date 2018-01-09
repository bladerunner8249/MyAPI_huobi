# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 11:28:31 2018

@author: Zeyu
"""

class HuobiAPIException(Exception):
    
    def __init__(self,response):
        json_res = response.json()
        self.status_code= response.status_code
        self.message = json_res['msg']
        self.code = json_res['code']
    
    def __str__(self):
        return 'API Error(code=%s): %s' % (self.code,self.message)


class HuobiRequestException(Exception):
    def __init__(self,message):
        self.message = message
    
    def __str__(self):
        return 'HuobiRequestException: %s' % self.message