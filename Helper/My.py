import requests
from dotenv import load_dotenv
import os
import time
import hmac
import hashlib

# Load environment variables from the .env file (if present)
load_dotenv()

try:
    from urllib import urlencode
# python3
except ImportError:
    from urllib.parse import urlencode


class My:

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def _get_no_sign(self, path, params=None):
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        print(query + " " + str(params))
        return requests.get(url, timeout=30, verify=True)

    def _get(self, path, params={}):
        params.update({"recvWindow": "500"})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.get(url, headers=header, timeout=30, verify=True)

    def _sign(self, params={}):
        data = params.copy()

        ts = int(1000 * time.time())
        data.update({"timestamp": ts})
        h = urlencode(data)
        b = bytearray()
        b.extend(self.secret.encode())
        signature = hmac.new(b, msg=h.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        data.update({"signature": signature})
        return data

    def _post(self, path, params={}):
        params.update({"recvWindow": os.getenv("REC_V_WINDOW")})
        query = urlencode(self._sign(params))
        url = "%s" % path
        header = {"X-MBX-APIKEY": self.key}
        return requests.post(url, headers=header, data=query, timeout=30, verify=True)

    def _order(self, market, quantity, side, rate=None):
        params = {}

        if rate is not None:
            params["type"] = "LIMIT"
            params["price"] = self._format(rate)
            params["timeInForce"] = "GTC"
        else:
            params["type"] = "MARKET"
        params["symbol"] = market
        params["side"] = side
        params["quantity"] = '%.8f' % quantity

        return params

    @staticmethod
    def _format(price):
        return "{:.8f}".format(price)
