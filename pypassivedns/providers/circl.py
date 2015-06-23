# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import json
import re
import datetime
import time

class Circl(Provider):
    NAME = "CIRCL"
    CONF = "circl"
    OPTL = "c"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.username = options.get("username", None)
        self.password = options.get("password", None)
        self.auth_token = options.get("auth_token", None)
        self.url = options.get("url", "https://www.circl.lu/pdns/query/")
        
        
    def query(self, query, limit=None):
        url = self.url + query
        params = {}
        
        headers = {}
        if self.username:
            headers = Provider.make_auth_header(self.username, self.password)
        
        if self.auth_token:
            headers["Authorization"] = self.auth_token
        
        start_time = time.time()
        data = Provider.get_json(url, "GET", params, headers, True)
        response_time = time.time() - start_time
        return self._data_to_records(query, data, response_time)
        
    @staticmethod
    def _data_to_records(query, data, response_time):
        recs = []
        for row in data:            
            query = row.get('rrname', '')
            answer = row.get('rdata')
            rrtype = row.get('rrtype', 'A')
            firstseen = datetime.datetime.utcfromtimestamp(int(row.get('time_first', '0')))
            lastseen = datetime.datetime.utcfromtimestamp(int(row.get('time_last', '0')))
            count = row.get('count', '0')
            recs.append(
                PDNSResult(Circl.NAME, response_time, query, answer, rrtype, 0, firstseen, lastseen, count)
            )
                 
        return recs