# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import json
import re
import datetime
import time

class TCPIPUtils(Provider):
    NAME = "TCPIPUtils"
    CONF = "tcpiputils"
    OPTL = "t"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.apikey = options.get("apikey")
        self.url = options.get("url", "https://www.utlsapi.com/api.php")
        
    def query(self, query, limit=None):
        params = {"apikey" : self.apikey, "version" : "1.0", "q" : query}
        if re.match("[\d\.]+$", query):
            params["type"] = "domainneighbors"
        else:
            params["type"] = "domainipdnshistory"
        
        start_time = time.time()
        reply_data = Provider.get_json(self.url, "GET", params)
        response_time = time.time() - start_time
        return self._data_to_records(query, reply_data, response_time)
        
    @staticmethod
    def _data_to_records(query, reply_data, response_time):
        recs = []
        fieldname = None
        rrtype = None
        add_records = False
        for key in reply_data["data"].keys():
            add_records = False
            data = reply_data["data"][key]
            if key == "ipv4":
                fieldname = "ip"
                rrtype = "A"
                add_records = True
            elif key == "ipv6":
                fieldname = "ip"
                rrtype = "AAAA"
                add_records = True
            elif key == "dns":
                fieldname = "dns"
                rrtype = "NS"
                add_records = True
            elif key == "mx":
                fieldname = "dns"
                rrtype = "MX"
                add_records = True
            elif key == "domains":
                for rec in data:
                    lastseen = datetime.datetime.strptime(rec.get("updatedate"), "%Y-%m-%d")
                    recs.append(PDNSResult(TCPIPUtils.NAME, response_time, rec, query, "A", None, None, lastseen, None))
            if add_records:
                for rec in data:
                    lastseen = datetime.datetime.strptime(rec.get("updatedate"), "%Y-%m-%d")
                    recs.append(PDNSResult(TCPIPUtils.NAME, response_time, query, rec[fieldname], rrtype, None, None, lastseen, None))
        return recs
        
                
                