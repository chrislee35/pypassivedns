import urllib.parse
import urllib.request
import json
import base64

class Provider:
    def name():
        pass
    
    def conf_name():
        pass
    
    def option_letter():
        pass
    
    def query(self, label, limit=None):
        pass

    @staticmethod
    def get_html(url, method, params={}, extraheaders={}):
        headers = { "User-Agent" : "pypassivedns v0.0.1", "Accept" : 'text/html', 'Content-Type' : 'text/html' }
        for key in extraheaders.keys():
            headers[key] = extraheaders[key]

        data = None
        if method == "POST":
            data = bytes(urllib.parse.urlencode(params), "utf-8")
        else:
            url = "%s?%s" % (url, urllib.parse.urlencode(params))
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        the_page = response.read().decode("ISO-8859-15")
        return the_page;

    @staticmethod
    def get_json(url, method, params={}, extraheaders={}, splitlines=False):
        headers = { "User-Agent" : "pypassivedns v0.0.1", "Accept" : 'Application/JSON', 'Content-Type' : 'Application/JSON' }
        for key in extraheaders.keys():
            headers[key] = extraheaders[key]

        data = None
        if method == "POST":
            data = bytes(urllib.parse.urlencode(params), "utf-8")
        else:
            url = "%s?%s" % (url, urllib.parse.urlencode(params))

        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        the_page = response.read().decode("utf-8")
        #print(the_page)
        jdata = []
        if splitlines:
            for line in the_page.split("\n"):
                if line:
                    jdata.append(json.loads(line))
        else:
            jdata = json.loads(the_page)
        
        return jdata
        
    @staticmethod
    def make_auth_header(username, password):
        base64string = base64.encodebytes(bytes('%s:%s' % (username, password), 'ascii'))[:-1].decode()
        authheader =  "Basic %s" % base64string
        return { "Authorization" : authheader }
