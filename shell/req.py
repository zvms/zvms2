from urllib.request import urlopen, Request
from urllib.error import URLError
import json

class Requester:
    def __init__(self, domain, headers):
        self.__domain = domain
        self.__headers = headers

    def __getattr__(self, method):
        return lambda url, **data: Requester.__request(self.__domain + url,
            json.dumps(data).encode(), self.__headers, method.upper())
        
    def __request(url, data, headers, method):
        try:
            req = Request(url, headers=headers, method=method)
            if data:
                res = json.load(urlopen(req, data))
            else:
                res = json.load(urlopen(req))
            print(res['message'])
            if res['type'] == 'SUCCESS':
                return res.get('result')
            for k, v in res.items():
                if k not in ('type', 'message'):
                    print(k, v)
            return None
        except URLError as ex:
            print(ex.reason)

headers = {}
req = Requester('http://127.0.0.1:1145', headers)