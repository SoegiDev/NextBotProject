from Helper.Response import *
from Helper.My import *
from dotenv import load_dotenv
import os

try:
    from urllib.parse import urlencode
# python3
except ImportError:
    from urllib.parse import urlencode


class Api:

    def __init__(self, key, secret):
        self.BASE_URL = os.getenv("BASE_URL_V3")
        if os.getenv("ENV") == "development":
            self.BASE_URL = os.getenv("BASE_URL_V3_DEV")
        self.key = key
        self.secret = secret
        self.my = My(key, secret)

    def ping(self):
        path = "%s/ping" % self.BASE_URL
        return self._get_no_sign(path, {})

    def get_server_time(self):
        path = "%s/time" % self.BASE_URL
        return self._get_no_sign(path)

    def get_history(self, market, limit=50):
        path = "%s/historicalTrades" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)

    def get_trades(self, market, limit=50):
        path = "%s/trades" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)

    def get_klines(self, market, interval, start_time, end_time):
        path = "%s/klines" % self.BASE_URL
        params = {"symbol": market, "interval": interval, "startTime": start_time, "endTime": end_time}
        return self._get_no_sign(path, params)

    def get_ticker(self, market):
        params = {}
        path = "%s/ticker/24hr" % self.BASE_URL
        if market is not None:
            params = {"symbol": market}
        return self._get_no_sign(path, params)

    def get_order_books(self, market, limit=50):
        path = "%s/depth" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)

    def get_account(self):
        path = "%s/account" % self.BASE_URL
        return self._get(path, {})

    def get_products(self):
        res_symbol = []
        path = "%s/exchangeInfo" % self.BASE_URL
        response = self._get_no_sign(path, {})
        for s in response.json()['symbols']:
            res_symbol.append(s['symbol'])
        return res_symbol

    def get_exchange_info(self):
        path = "%s/exchangeInfo" % self.BASE_URL
        return self._get_no_sign(path)

    def get_open_orders(self, market):
        params = {}
        if market is not None:
            params = {"symbol": market}
        path = "%s/openOrders" % self.BASE_URL
        return self._get(path, params)

    def get_my_trades(self, market, limit=50):
        params = {}
        path = "%s/myTrades" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get(path, params)

    def buy_limit(self, market, quantity, rate):
        params = {}
        path = "%s/order" % self.BASE_URL
        params = self._order(market, quantity, "BUY", rate)
        return self._post(path, params)

    def sell_limit(self, market, quantity, rate):
        path = "%s/order" % self.BASE_URL
        params = self._order(market, quantity, "SELL", rate)
        return self._post(path, params)

    def buy_market(self, market, quantity):
        path = "%s/order" % self.BASE_URL
        params = self._order(market, quantity, "BUY")
        return self._post(path, params)

    def sell_market(self, market, quantity):
        path = "%s/order" % self.BASE_URL
        params = self._order(market, quantity, "SELL")
        return self._post(path, params)

    def query_order(self, market, order_id):
        path = "%s/order" % self.BASE_URL
        params = {"symbol": market, "orderId": order_id}
        return self._get(path, params)

    def query_all_order_list(self, startTime, endTime):
        path = "%s/allOrderList" % self.BASE_URL
        params = {"startTime": startTime, "endTime": endTime}
        return self._get(path, params)

    def query_order_all(self, market):
        path = "%s/allOrders" % self.BASE_URL
        params = {"symbol": market}
        return self._get(path, params)

    def cancel(self, market, order_id):
        path = "%s/order" % self.BASE_URL
        params = {"symbol": market, "order_id": order_id}
        return self._delete(path, params)

    @staticmethod
    def _get_no_sign(path, params=None):
        if params is None:
            params = {}
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        return requests.get(url, timeout=5, verify=True)

    def _sign(self, params=None):
        if params is None:
            params = {}
        data = params.copy()
        ts = int(1000 * time.time())
        data.update({"timestamp": ts})
        h = urlencode(data)
        b = bytearray()
        b.extend(self.secret.encode())
        signature = hmac.new(b, msg=h.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        data.update({"signature": signature})
        return data

    def _get(self, path, params=None):
        if params is None:
            params = {}
        params.update({"recvWindow": os.getenv("REC_V_WINDOW")})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.get(url, headers=header, timeout=20, verify=True)

    def _post(self, path, params=None):
        if params is None:
            params = {}
        params.update({"recvWindow": os.getenv("REC_V_WINDOW")})
        query = urlencode(self._sign(params))
        url = "%s" % path
        header = {"X-MBX-APIKEY": self.key}
        return requests.post(url, headers=header, data=query, timeout=20, verify=True)

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

    def _delete(self, path, params=None):
        if params is None:
            params = {}
        params.update({"recvWindow": os.getenv("REC_V_WINDOW")})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.delete(url, headers=header, timeout=20, verify=True)

    def _format(self, price):
        return "{:.8f}".format(price)
