# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:57:09 2017

@author: Zeyu
"""

import pymongo
import time
import traceback
from pymongo.helpers import DuplicateKeyError
from datetime import datetime
from huobi_API import Quotes

CONNECTOIN = pymongo.MongoClient('192.168.0.22',27017)

def comb(ts,kline):
    head = ts/1000
    tail = ts%1000
    normal_time = datetime.fromtimestamp(head).strftime('%Y-%m-%d %H:%M:%S')
    normal_time  = normal_time+'.'+str(tail)
    kline['_id'] = normal_time   
    return kline

def writeMongo(instance,dbName):
    info = instance.kline('1min',1)        
    ts = info['ts']; data = info['data'][0]
    conn = CONNECTOIN[dbName]
    table = conn[instance.get_attribute()]
    x = data.copy()
    #print x
    table.insert_one(comb(ts,x))  
    
if __name__ == "__main__":
    BTC = Quotes('btcusdt')
    ETH = Quotes('ethusdt')
    ETC = Quotes('etcusdt')
    BCH = Quotes('bchusdt')
    
    dbName = 'huobi'
    
    #while True:
    for i in range(10):
        try:
            writeMongo(BTC,dbName)
            time.sleep(1)
            writeMongo(ETH,dbName)
            time.sleep(1)
            writeMongo(ETC,dbName)
            time.sleep(1)
            writeMongo(BCH,dbName)
            time.sleep(1)
        except DuplicateKeyError:
            time.sleep(25)
        except:
            now = str(datetime.now())
            errorFile = open('huobi_error.txt','a')
            errorFile.write(now+'\n')
            errorFile.write(traceback.format_exc())
            errorFile.write("\n \n")
            errorFile.close()
        
            