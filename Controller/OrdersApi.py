from Helper.Api import *
from Function.Orders import *
from Helper.Database import *
import datetime
import time


class OrdersApi:

    def __init__(self, key, secret, username):
        self.client = Api(key, secret)
        self.orderSpot = Orders(key, secret)
        self.username = username

    def get_price(self, symbol):
        data_result = []
        try:
            response = self.client.get_ticker(symbol).json()
            if 'msg' in response:
                return Response.get_res(400, response['msg'], 1)
            for s in response:
                if s['symbol'].endswith('USDT'):
                    data_result.append(s)
            return Response.get_res(200, data_result, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def get_price_lite(self):
        data_result = []
        symbol = None
        try:
            response = self.client.get_ticker(symbol).json()
            if 'msg' in response:
                Messages.get(response['msg'])
            for s in response:
                if s['symbol'].endswith('USDT'):
                    data_result.append(s['symbol'])
            return data_result
        except Exception as e:
            print('cancel_order Exception: %s' % e)
            return False

    def get_info(self, symbol):
        try:
            symbol_param = "";
            if symbol is not None:
                symbol_param = symbol
            response = self.client.get_exchange_info().json()
            if 'msg' in response:
                return Response.get_res(400, response['msg'], 1)
            if symbol_param != "":
                data_result = [market for market in response['symbols'] if market['symbol'] == symbol][0]
                return Response.get_res(200, data_result, 0)
            return Response.get_res(200, response, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def get_order(self, symbol, orderId):
        try:
            if symbol is None:
                return Response.get_res(400, "Symbol Not Filled", 1)
            if orderId is None:
                return Response.get_res(400, "Order Id Not Filled", 1)
            response = self.client.query_order(symbol, orderId).json()
            if 'msg' in response:
                return Response.get_res(400, response['msg'], 1)
            return Response.get_res(200, response, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def get_order_status(self, symbol, orderId):
        try:
            if symbol is None:
                return Response.get_res(400, "Symbol Not Filled", 1)
            response = self.client.query_order(symbol, orderId).json()
            if 'msg' in response:
                return Response.get_res(400, response['msg'], 1)
            return Response.get_res(200, response['status'], 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def get_order_all(self, symbol):
        try:
            if symbol is None:
                return Response.get_res(400, "Symbol Not Filled", 1)
            #response = self.client.query_order_all(symbol)
            order = self.client.query_order_all(symbol).json()
            if 'msg' in order:
                return Response.get_res(400, order['msg'], 1)
            return Response.get_res(200, order, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def get_open_orders(self):
        try:
            #response = self.client.query_order_all(symbol)
            order = self.client.get_open_orders(None).json()
            if 'msg' in order:
                return Response.get_res(400, order['msg'], 1)
            return Response.get_res(200, order, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def get_all_order_list(self, startTime, endTime):
        try:
            #response = self.client.query_order_all(symbol)
            order = self.client.query_all_order_list(startTime, endTime).json()
            if 'msg' in order:
                return Response.get_res(400, order['msg'], 1)
            return Response.get_res(200, order, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def get_all_order_market(self):
        try:
            coins = self.get_price_lite()
            get = 0
            for i in coins:
                traded = []
                order = self.client.get_my_trades(i).json()
                if 'msg' in order:
                    return Response.get_res(400, order['msg'], 1)
                if order:
                    get = get + 1
                    for j in order:
                        traded.append(j)
                        print(f'Ada Order maker {j}')
                else:
                    print(f'Tidak Ada Order maker {i}')
                time.sleep(0.5)
                if get >= 5 :
                    return Response.get_res(200, traded, 0)

        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)
