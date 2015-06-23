# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import json
import re
import datetime
import time

class RiskIQ(Provider):
    NAME = "RiskIQ"
    CONF = "riskiq"
    OPTL = "r"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.token = options.get("api_token", None)
        self.privkey = options.get("api_private_key", None)
        self.server = options.get("api_server", "ws.riskiq.net")
        self.version = options.get("api_version", "v1")
        self.url = "https://%s/%s" % (self.server, self.version)
        
    def query(self, query, limit=None):
        url = None
        params = {"rrType" : "", "maxResults" : limit or 1000}
        if re.match("[\d\.]+$", query):
            url = "%s/dns/data" % self.url
            params["ip"] = query
        else:
            url = "%s/dns/name" % self.url
            params["name"] = query

        start_time = time.time()
        data = Provider.get_json(url, "GET", params, Provider.make_auth_header(self.token, self.privkey))
        response_time = time.time() - start_time
        return self._data_to_records(query, data, response_time)
        
    @staticmethod
    def _data_to_records(query, data, response_time):
        recs = []
        for row in data.get("records", []):
            name = row.get("name", '')
            name = re.sub('\.$', '', name)
            t = row.get("rrtype", "A")
            lastseen = datetime.datetime.strptime(row.get('lastSeen'), "%Y-%m-%dT%H:%M:%S.000%z")
            firstseen = datetime.datetime.strptime(row.get('firstSeen'), "%Y-%m-%dT%H:%M:%S.000%z")
            count = row.get("count", 0)
            for datum in row["data"]:
                datum = re.sub('\.$', '', datum)
                recs.append(PDNSResult(RiskIQ.NAME, response_time, name, datum, t, 0, firstseen, lastseen, count))

        return recs
                
                