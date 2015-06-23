# -*- coding: utf-8 -*-

from pypassivedns.provider import Provider
from pypassivedns.pypassivedns import PDNSResult
import datetime
import time
import re

class BFK(Provider):
    NAME = "BFK.de"
    CONF = "bfk"
    OPTL = "b"
    
    def __init__(self, options={}):
        self.debug = options.get("debug", False)
        self.url = options.get("url", "http://www.bfk.de/bfk_dnslogger.html")
        
        
    def query(self, query, limit=None):
        url = self.url
        params = {"query" : query}
        
        start_time = time.time()
        data = Provider.get_html(url, "GET", params)
        response_time = time.time() - start_time
        return self._data_to_records(query, data, response_time)
        
    @staticmethod
    def _data_to_records(query, data, response_time):
        recs = []
        html = re.sub("\n", '', data)
        ress=re.findall("<table id=\"logger\".*?\/table>", html)
        if len(ress) != 1:
            return recs;
        table = ress[0]
        table = re.sub("\t", '', table)
        table = re.sub("<td>", '\t', table)
        table = re.sub("</tr>", '\n', table)
        table = re.sub("<.*?>", '', table)
        table = re.sub("&nbsp;", '', table)
        table = re.sub("\n\t", "\n", table)
        table = re.sub("^\t", '', table)
        rows = table.split("\n")
        for row in rows:
            fields = row.split("\t")
            if len(fields) == 3:
                query, rrtype, answer = fields
            elif len(fields) == 4:
                query, rrtype, weight, answer = fields
            recs.append(
                PDNSResult(BFK.NAME, response_time, query, answer, rrtype, 0, '', '', 0)
            )

        return(recs)
