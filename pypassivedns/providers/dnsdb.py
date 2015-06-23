# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import json
import re
import datetime
import time

class DNSDB(Provider):
    NAME = "DNSDB"
    CONF = "dnsdb"
    OPTL = "d"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.apikey = options.get("apikey", None)
        self.url = options.get("url", "https://api.dnsdb.info/lookup")
        
        
    def query(self, query, limit=None):
        url = None
        if re.match("[\d\.]+$", query):
            url = "%s/rdata/ip/%s" % (self.url, query)
        else:
            url = "%s/rrset/name/%s" % (self.url, query)
        params = {}
        if limit:
            params["limit"] = limit
        start_time = time.time()
        
        data = Provider.get_json(url, "GET", params, { "X-API-Key" : self.apikey }, True)
        response_time = time.time() - start_time
        return self._data_to_records(query, data, response_time)
        
    @staticmethod
    def _data_to_records(query, data, response_time):
        recs = []
        for row in data:
            answers = row.get('rdata')
            if type(answers) == str:
                answers = [answers]
            query = row.get('rrname', '')
            query = re.sub('\.$', '', query)
            rrtype = row.get('rrtype', 'A')
            firstseen = datetime.datetime.utcfromtimestamp(int(row.get('time_first', '0')))
            lastseen = datetime.datetime.utcfromtimestamp(int(row.get('time_last', '0')))
            count = row.get('count', '0')
            for answer in answers:
                recs.append(
                    PDNSResult(DNSDB.NAME, response_time, query, answer, rrtype, 0, firstseen, lastseen, count)
                )
        return recs