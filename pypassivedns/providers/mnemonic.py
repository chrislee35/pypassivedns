# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import json
import re
import datetime
import time

class Mnemonic(Provider):
    NAME = "Mnemonic"
    CONF = "mnemonic"
    OPTL = "m"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.apikey = options.get("apikey", None)
        self.url = options.get("url", "https://passivedns.mnemonic.no/api1/")
        
        
    def query(self, query, limit=None):
        url = self.url+self.apikey
        params = {"query" : query, "method" : "exact" }
        start_time = time.time()
        data = Provider.get_json(url, "GET", params)
        response_time = time.time() - start_time
        return self._data_to_records(query, data, response_time)
        
    @staticmethod
    def _data_to_records(query, data, response_time):
        recs = []
        if data.get("result", None):
            for row in data.get("result", []):
                query = row.get("query", '')
                answer = row.get("answer", '')
                rrtype = row.get("type", '').upper()
                tty = row.get("ttl", "0")
                firstseen = datetime.datetime.utcfromtimestamp(int(row.get('first', '0')))
                lastseen = datetime.datetime.utcfromtimestamp(int(row.get('last', '0')))
                recs.append(PDNSResult(Mnemonic.NAME, response_time, query, answer, rrtype, tty, firstseen, lastseen, 0))
        return recs