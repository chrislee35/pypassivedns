#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pypassivedns
----------------------------------

Tests for `pypassivedns` module.
"""

import unittest
import os
import configparser

from pypassivedns import pypassivedns
from pypassivedns.providers.virustotal import VirusTotal
from pypassivedns.providers.tcpiputils import TCPIPUtils
from pypassivedns.providers.riskiq import RiskIQ
from pypassivedns.providers.passivetotal import PassiveTotal
from pypassivedns.providers.mnemonic import Mnemonic
from pypassivedns.providers.dnsdb import DNSDB
from pypassivedns.providers.cn360 import CN360
from pypassivedns.providers.circl import Circl
from pypassivedns.providers.bfk import BFK

class TestPypassivedns(unittest.TestCase):
    
    def setUp(self):
        try:
            self.config
        except AttributeError:
            configfilename = "%s/.passivedns-client" % os.environ["HOME"]
            configfh = open(configfilename)
            conf = configfh.read()
            configfh.close()
            #conf = conf
            p = configparser.ConfigParser()
            p.read_string(conf)
            self.config = {}
            for section in p.sections():
                self.config[section] = {}
                for item in p[section].items():
                    self.config[section][item[0]] = item[1]

    def test_pdnsresult(self):
        record = pypassivedns.PDNSResult("test", "0.0", "example.com", "1.2.3.4", "A", 10, None, None, 1)
        
    def test_virustotal(self):
        return
        klass = VirusTotal
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)
    
    def test_tcpiputils(self):
        return
        klass = TCPIPUtils
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)
        
    def test_riskiq(self):
        return
        klass = RiskIQ
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)

    def test_passivetotal(self):
        return
        klass = PassiveTotal
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)

    def test_mnemonic(self):
        return
        klass = Mnemonic
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)

    def test_dnsdb(self):
        return
        klass = DNSDB
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)

    def test_cn360(self):
        return
        klass = CN360
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)

    def test_circl(self):
        return
        klass = Circl
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)

    def test_bfk(self):
        klass = BFK
        provider = klass(self.config.get(klass.CONF, {}))
        recs = provider.query("example.org")
        for rec in recs:
            print(rec)
            
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
