# -*- coding: utf-8 -*-
import threading
import datetime

class PDNSResult:
    def __init__(self, source, response_time, query, answer, rrtype, ttl, firstseen, lastseen, count):
        self.source = source
        self.response_time = response_time
        self.query = query
        self.answer = answer
        self.rrtype = rrtype
        self.ttl = ttl
        self.firstseen = firstseen
        self.lastseen = lastseen
        self.count = count
    
    def __str__(self):
        return "%s,%0.2f,%s,%s,%s,%d,%s,%s,%d" % (
            self.source,
            self.response_time,
            self.query,
            self.answer, 
            self.rrtype or 'A', 
            self.ttl or 0,
            PDNSResult.datetime_utc_str(self.firstseen),
            PDNSResult.datetime_utc_str(self.lastseen),
            self.count or 0
        )
    
    @staticmethod
    def datetime_utc_str(dt):
        if dt:
            return datetime.datetime.utcfromtimestamp(dt.timestamp())
        return ''
    

class Client:
    def __init__(self, providers):
        self.providers = providers

    def query(self, item, limit=None):
        threads = []
        for provider in self.providers:
            t = threading.Thread(target=_query, args=(provider, item, limit))
            threads.append(t)
            t.start()
        
        res = []
        for thread in threads:
            res.append(thread.join())
        
    def _query(provider, item, limit=None):
        res = provider.query(item, limit)
        return res

