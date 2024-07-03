
from Helper.Api import *
from Helper.Message import Messages


class Orders:

    def __init__(self, key, secret):
        self.client = Api(key, secret)

    def buy_limit(self, symbol, quantity, buy_prices):

        order = self.client.buy_limit(symbol, quantity, buy_prices).json()

        if 'msg' in order:
            Messages.get(order['msg'])

        # Buy order created.
        return order['orderId']

    def sell_limit(self, symbol, quantity, sell_price):

        order = self.client.sell_limit(symbol, quantity, sell_price).json()

        if 'msg' in order:
            Messages.get(order['msg'])

        return order

    def buy_market(self, symbol, quantity):

        order = self.client.buy_market(symbol, quantity).json()

        if 'msg' in order:
            Messages.get(order['msg'])

        return order

    def sell_market(self, symbol, quantity):

        order = self.client.sell_market(symbol, quantity).json()

        if 'msg' in order:
            Messages.get(order['msg'])

        return order

    def cancel_order(self, symbol, order_id):

        try:

            order = self.client.cancel(symbol, order_id).json()
            if 'msg' in order:
                Messages.get(order['msg'])

            print('Profit loss, called order, %s' % order_id)

            return True

        except Exception as e:
            print('cancel_order Exception: %s' % e)
            return False

    def get_order_book(self, symbol):
        try:

            orders = self.client.get_order_books(symbol, 5).json()
            last_bid = float(orders['bids'][0][0])  # last buy price (bid)
            last_ask = float(orders['asks'][0][0])  # last sell price (ask)

            return last_bid, last_ask

        except Exception as e:
            print('get_order_book Exception: %s' % e)
            return 0, 0

    def get_order(self, symbol, order_id):
        try:

            order = self.client.query_order(symbol, order_id).json()

            if 'msg' in order:
                # import ipdb; ipdb.set_trace()
                Messages.get(order['msg'])  # TODO
                return False

            return order

        except Exception as e:
            print('get_order Exception: %s' % e)
            return False

    def get_order_all(self, symbol):
        try:

            order = self.client.query_order_all(symbol).json()

            if 'msg' in order:
                # import ipdb; ipdb.set_trace()
                Messages.get(order['msg'])  # TODO
                return False

            return order

        except Exception as e:
            print('get_order Exception: %s' % e)
            return False

    def get_order_status(self, symbol, order_id):
        try:

            order = self.client.query_order(symbol, order_id).json()

            if 'msg' in order:
                Messages.get(order['msg'])

            return order['status']

        except Exception as e:
            print('get_order_status Exception: %s' % e)
            return None

    def get_ticker(self, symbol):
        try:

            ticker = self.client.get_ticker(symbol).json()

            return float(ticker['lastPrice'])
        except Exception as e:
            print('Get Ticker Exception: %s' % e)

    def get_info(self, symbol):
        try:

            info = self.client.get_exchange_info().json()

            if symbol != "":
                return [market for market in info['symbols'] if market['symbol'] == symbol][0]

            return info

        except Exception as e:
            print('get_info Exception: %s' % e)
