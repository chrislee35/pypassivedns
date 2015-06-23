# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import json
import re
import datetime
import time
import hashlib

class CN360(Provider):
    NAME = "360.cn"
    CONF = "cn360"
    OPTL = "3"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.apikey = options.get("api_key", None)
        self.apiid = options.get("api_id", None)
        self.url = options.get("api", None)
        
        
    def query(self, query, limit=None):
        table = "rrset"
        if re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", query) or re.match("[0-9a-fA-F]+:[0-9a-fA-F:]+[0-9a-fA-F]$", query):
            table = "rdata"
        limit = limit or 1000
        path = "/api/%s/keyword/%s/count/%s/" % (table, query, limit)
        url = self.url + path
        
        md5 = hashlib.md5()
        
        md5.update((path + self.apikey).encode('utf-8'))
        token = md5.hexdigest()
        headers = { "X-BashTokid" : self.apiid, "X-BashToken" : token }
        params = {}
        start_time = time.time()
        data = Provider.get_json(url, "GET", params, headers)
        response_time = time.time() - start_time
        return self._data_to_records(query, data, response_time)
        
    @staticmethod
    def _data_to_records(query, data, response_time):
        recs = []
        for row in data:
            firstseen = datetime.datetime.utcfromtimestamp(int(row.get('time_first', '0')))
            lastseen = datetime.datetime.utcfromtimestamp(int(row.get('time_last', '0')))
            count = row.get("count", 0)
            query = row.get("rrname", '')
            answers = row.get("rdata", '')
            answers = re.sub(';$', '', answers)
            answers = answers.split(";")
            rrtype = row.get("rrtype")
            for answer in answers:
                recs.append(
                    PDNSResult(CN360.NAME, response_time, query, answer, rrtype, 0, firstseen, lastseen, count)
                )
        return recs
