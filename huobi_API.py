# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:50:28 2017

@author: Administrator
"""
from huobi_util import httpGET, httpPOST,sign
from datetime import datetime
import urllib
import urlparse

accesskey = ''
secretkey = ''
acctID  = 123456
class Quotes:
    '''
    用于从https://api.huobi.pro获取行情
    symbol:'btcusdt', 'ethusdt','etcusdt', 'bchusdt'
    '''
    def __init__(self,symbol):
        self.__host = 'https://api.huobi.pro'
        self.__symbol = symbol
    
    def get_attribute(self):
        return self.__symbol
    
    #获取现货市场行情
    def kline(self,period='',size=150):        
        #period:1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
        PATH = "/market/history/kline"
        url = self.__host + PATH
        params={'size':size}
        params['symbol'] = self.__symbol
        if period:
            params['period'] = period        
        return httpGET(url,params)
    
    #获取Market Depth 数据
    def depth(self, _type='step1'):
        PATH = '/market/depth'
        url = self.__host + PATH
        params = {'type':_type}
        params['symbol'] = self.__symbol
        return httpGET(url,params)
    
    #获取聚合行情(Ticker)
    def merged(self):
        PATH = '/market/detail/merged'
        url = self.__host + PATH
        params = {'symbol':self.__symbol}
        return httpGET(url,params)
    
    #获取 Trade Detail 数据
    def latestDetail(self):
        PATH = '/market/trade'
        url = self.__host + PATH
        params = {'symbol':self.__symbol}
        return httpGET(url,params)
        
    #批量获取最近的交易记录
    def historyDetail(self,size=5):
        PATH = '/market/history/trade'
        url = self.__host + PATH
        params = {'size':size}
        params['symbol'] = self.__symbol
        return httpGET(url,params)
    
    #获取 Market Detail 24小时成交量数据
    def last24h(self):
        PATH = '/market/detail'
        url = self.__host + PATH
        params = {'symbol':self.__symbol}
        return httpGET(url,params)
        



class Account: 
    '''
    获取用户账户资产信息 
    '''
    def __init__(self,accesskey,secretkey):
        self.__host = 'https://api.huobi.pro'
        self.__accesskey = accesskey
        self.__secretkey = secretkey

    def _httpGET_key(self,params,path):
        ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self.__accesskey,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': ts})
        hostName = urlparse.urlparse(self.__host).hostname
        params['Signature'] = sign(params,'GET',hostName,path,self.__secretkey)
        url = self.__host + path        
        return httpGET(url, params)

    #查询当前用户的所有账户(即account-id)    
    def ID(self):
        PATH = '/v1/account/accounts'
        return self._httpGET_key({},PATH)
        
    #查询账户的余额
    def balance(self,acctID=876473):
        if not acctID:
            try:
                accounts = self.ID()
                acctID = ACCOUNT_ID = accounts['data'][0]['id']
            except BaseException as e:
                print 'get acct_id error.%s'%e
                acctID = ACCOUNT_ID
        PATH = "/v1/account/accounts/{0}/balance".format(acctID)
        params = {"account-id": acctID}
        return self._httpGET_key(params,PATH)



     
class Trade:
    '''
    指定特定账户，特定交易对交易
    账户ID需要事先获取   
    symbol: btcusdt, ethusdt,tcusdt, etcusdt, bccusdt
    type: buy-market市价买, sell-market市价卖, buy-limit限价买, sell-limit限价卖
    '''
    def __init__(self,symbol,accesskey,secretkey,acctID):
        self.__host = 'https://api.huobi.pro'
        self.__accesskey = accesskey
        self.__secretkey = secretkey
        self.__symbol = symbol
        self.__acctID = acctID #876473
    
    def _httpGET_key(self,params,path):
        ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self.__accesskey,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': ts})
        hostName = urlparse.urlparse(self.__host).hostname
        params['Signature'] = sign(params,'GET',hostName,path,self.__secretkey)
        url = self.__host + path        
        return httpGET(url, params)
        
    def _httpPOST_key(self,params,path):
        ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self.__accesskey,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': ts}
        hostName = urlparse.urlparse(self.__host).hostname
        params_to_sign['Signature'] = sign(params_to_sign,'POST',hostName,\
                                           path,self.__secretkey)
        url = self.__host + path + '?' + urllib.urlencode(params_to_sign)
        return httpPOST(url, params)
    
    #下单    
    def order(self,amount,symbol, _type, price=None):
        PATH = '/v1/order/orders/place'
        params = {"account-id": self.__acctID,
              "amount": amount,
              "symbol": self.__symbol,
              "type": _type}
        if price:
            params["price"] = price
        return self._httpPOST_key(params,PATH)
    
    #申请撤销一个订单请求    
    def cancel(self,order_id):
        PATH = "/v1/order/orders/{0}/submitcancel".format(order_id)        
        params = {}
        return self._httpPOST_key(params,PATH)
    
    #批量撤销订单
    def cancelbatch(self,order_ids_lst):
        PATH = '/v1/order/orders/batchcancel' 
        params = {'order-ids':order_ids_lst}
        return self._httpPOST_key(params,PATH)
    
    #查询某个订单详情
    def orderInfo(self,order_id):
        PATH = "/v1/order/orders/{0}".format(order_id)
        return self._httpPOST_key({},PATH)
    
    #查询某个订单的成交明细
    def matchresults(self,order_id):
        PATH = "/v1/order/orders/{0}/matchresults".format(order_id)
        return self._httpGET_key({},PATH)
    
    #查询本账户该交易对的当前委托、历史委托
    def orderHistory(self,states,types=None,start=None,end=None, _from=None,direct=None, size=None):
        """
        :param states:str,{pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}        
        :param types:str,{buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start: str,查询开始日期, 日期格式yyyy-mm-dd
        :param end: str,查询结束日期, 日期格式yyyy-mm-dd
        :param _from: str,查询起始 ID
        direct:str,{prev 向前，next 向后}
        """
        PATH = '/v1/order/orders'        
        params = {'symbol': self.__symbol,'states': states}
        if types:
            params[types] = types
        if start:
            params['start-date'] = start
        if end:
            params['end-date'] = end
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        return self._httpGET_key(params,PATH)
    
     #查询本账户当前交易对的当前成交、历史成交
    def matchHistory(self,types=None,start=None,end=None,_from=None,direct=None,size=None):
        PATH = '/v1/order/matchresults'
        params = {'symbol': self.__symbol}
        if types:
            params['types'] = types
        if start:
            params['start-date'] = start
        if end:
            params['end-date'] = end
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        return self._httpGET_key(params,PATH)
        
        
        
        
        
        
        
        
        
        
 
        
            
            
        
        
        
        
       
            
        
        
        
        
        
        
    
    
        
        
        
        
        
        