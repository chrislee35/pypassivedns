# -*- coding: utf-8 -*-

class PDNSResult:
    def __init__(self, source, response_time, query, answer, rrtype, ttl, firstseen, lastseen, count):
        self.source = source
        self.response_time = respsonse_time
        self.query = query
        self.answer = answer
        self.rrtype = rrtype
        self.ttl = ttl
        self.firstseen = firstseen
        self.lastseen = lastseen
        self.count = count
