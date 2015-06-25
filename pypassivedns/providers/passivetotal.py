# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import json
import re
import datetime
import time

class PassiveTotal(Provider):
    NAME = "PassiveTotal"
    CONF = "passivetotal"
    OPTL = "p"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.apikey = options.get("apikey", None)
        self.version = options.get("api_version", "v1")
        self.url = options.get("url", "https://www.passivetotal.org/api/%s/passive" % self.version)
        
    def query(self, query, limit=None):
        url = self.url
        params = {"api_key" : self.apikey, "query" : query}
        start_time = time.time()
        data = Provider.get_json(url, "GET", params)
        response_time = time.time() - start_time
        return self._data_to_records(query, data, response_time)
        
    @staticmethod
    def _data_to_records(query, data, response_time):
        recs = []
        if data.get("results", None):
            query = data.get("raw_query")
            for row in data.get("results").get("records", []):
                firstseen = datetime.datetime.strptime(row.get('firstSeen'), "%Y-%m-%d %H:%M:%S")
                lastseen = datetime.datetime.strptime(row.get('lastSeen'), "%Y-%m-%d %H:%M:%S")
                value = row.get("resolve")
                source = ','.join(row.get("source"))
                if re.match("[\d\.]+$", query):
                    recs.append(
                        PDNSResult("%s/%s" % (PassiveTotal.NAME, source), response_time, value, query, "A", 0, firstseen, lastseen, 0)
                    )
                else:
                    recs.append(
                        PDNSResult("%s/%s" % (PassiveTotal.NAME, source), response_time, query, value, "A", 0, firstseen, lastseen, 0)
                    )

        return recs                