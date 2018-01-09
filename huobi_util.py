# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 09:47:51 2017

@author: Zeyu
用于生成签名,以及 http 请求
"""
import requests
import json
import hashlib
import hmac
import base64
import urllib
import time
import urlparse
from huobi_exceptions import HuobiAPIException, HuobiRequestException


ACCESS_KEY = "4ca6d7ba-4b525188-bccc7dc9-0eac3"
SECRET_KEY = "ad15a1b0-5dc44bed-1a15e804-5ff4c"
LANG = 'zh-CN'

def _encode(s):
    return urllib.quote(s, safe='')

def sign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(),key=lambda d:d[0], reverse=False)
    encode_params = urllib.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature 

def handle_response(response):
    if not str(response.status_code).startswith('2'):
        raise HuobiAPIException(response)
    try:
        return response.json()
    except ValueError:
        raise HuobiRequestException('Invalid Response: %s' % response.text)
    except Exception as e:
            raise Exception("other response Exception: %s" %e)


def httpGET(url,params,add2headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'Accept-Language': LANG,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    }
    if add2headers:
        headers.update(add2headers)
    postdata = urllib.urlencode(params)
    response = requests.post(url, postdata,headers=headers,timeout=5) 
    try:
        response = requests.get(url, postdata,headers=headers,timeout=5)
        return handle_response(response)
    except requests.exceptions.ConnectionError as e:
        time.sleep(5)
        raise Exception("Connection refused : %s" %e)
    except Exception as e:
        raise Exception("Other request exception: %s" %e)
        

def httpPOST(url,params,add2headers=None):
    postdata = json.dumps(params)    
    headers = {
        "Accept": "application/json",
        'Accept-Language': LANG,
        'Content-Type': 'application/json',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    }
    if add2headers:
        headers.update(add2headers)   
    try:
        response = requests.post(url, postdata,headers=headers,timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status":response.status_code}
    except Exception as e:
        print("httpPost failed:%s" % e)
        return {"status":"fail","msg":e}
  