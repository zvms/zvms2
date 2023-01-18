import json

import requests

class Requester:
    def __init__(self, domain, headers):
        self.__domain = domain
        self.__headers = headers

    def __getattr__(self, method):
        return lambda url, echo=True, **data: Requester.__request(self.__domain + url,
            echo, json.dumps(data).encode() if data else None, self.__headers, method.upper())
        
    def __request(url, echo, data, headers, method):
        res = requests.__getattribute__(method.lower())(url, data=data, headers=headers)
        status_code = res.status_code
        try:
            res = json.loads(res.text)
        except json.decoder.JSONDecodeError:
            print(res.text)
            return
        if echo:
            if status_code // 100 != 2:
                print(status_code, end=' ')
            print(res['message'])
        if res['type'] == 'SUCCESS':
            return res.get('result')
        for k, v in res.items():
            if k not in ('type', 'message'):
                print(k, v)
        return None

headers = {}
req = Requester('http://127.0.0.1:1145', headers)