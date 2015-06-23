# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import json
import re
import datetime
import time

class VirusTotal(Provider):
    NAME = "VirusTotal"
    CONF = "virustotal"
    OPTL = "v"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.apikey = options.get("apikey")
        self.url = options.get("url","https://www.virustotal.com/vtapi/v2/")
        
    def query(self, query, limit=None):
        url = None
        params = {"apikey" : self.apikey}
        if re.match("[\d\.]+$", query):
            url = "%sip-address/report" % self.url
            params["ip"] = query
        else:
            url = "%sdomain/report" % self.url
            params["domain"] = query
        
        start_time = time.time()
        data = Provider.get_json(url, "GET", params)
        response_time = time.time() - start_time
        return self._data_to_records(query, data, response_time)
        
    @staticmethod
    def _data_to_records(query, data, response_time):
        res = []
        for row in data.get("resolutions", []):
            lastseen = datetime.datetime.strptime(row.get('last_resolved'), "%Y-%m-%d %H:%M:%S")
            if row.get("ip_address", None):
                res.append(
                    PDNSResult(VirusTotal.NAME, response_time, query, row.get("ip_address"), 'A', None, None, lastseen, 1)
                )
            elif row.get("hostname", None):
                res.append(
                    PDNSResult(VirusTotal.NAME, response_time, row.get("hostname"), query, 'A', None, None, lastseen, 1)
                )
        return res
        
                
                