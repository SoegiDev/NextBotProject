from Helper.Api import *
from datetime import timedelta, datetime


class Balance:

    def __init__(self, key, secret):
        self.client = Api(key, secret)

    def balances(self):
        balances = self.client.get_account().json()
        for balance in balances['balances']:
            if float(balance['locked']) > 0 or float(balance['free']) > 0:
                print('%s: %s' % (balance['asset'], balance['free']))

    def balance(self, asset='BTC'):
        balances = self.client.get_account().json()
        balances['balances'] = {item['asset']: item for item in balances['balances']}
        print(balances['balances'][asset]['free'])

    def orders(self, symbol):
        orders = self.client.get_open_orders(symbol).json()
        print(orders)

    def server_status(self):
        system_t = int(time.time() * 1000)  # timestamp when requested was launch
        server_t = self.client.get_server_time().json()  # timestamp when server replied
        lag = int(server_t['serverTime'] - system_t)

        print(f"System timestamp: {system_t}")
        print(f"Server timestamp: {server_t['serverTime']}")
        print(f"Lag: {lag}")

        if lag > 1000:
            print('Not good. Excessive lag (lag > 1000ms)')
        elif lag < 0:
            print('Not good. System time ahead server time (lag < 0ms)')
        else:
            print('Good (0ms > lag > 1000ms)')
        return

    def open_orders(self):

        return self.client.get_open_orders(None)

    def profits(self, asset='BTC'):
        coins = self.client.get_products()

        for coin in coins['data']:
            if coin['quoteAsset'] == asset:
                orders = self.client.get_order_books(coin['symbol'], 5)
                if len(orders['bids']) > 0 and len(orders['asks']) > 0:
                    lastBid = float(orders['bids'][0][0])  # last buy price (bid)
                    lastAsk = float(orders['asks'][0][0])  # last sell price (ask)

                    if lastBid != 0:
                        profit = (lastAsk - lastBid) / lastBid * 100
                    else:
                        profit = 0
                    print('%6.2f%% profit : %s (bid: %.8f / ask: %.8f)' % (profit, coin['symbol'], lastBid, lastAsk))
                else:
                    print('---.--%% profit : %s (No bid/ask info retrieved)' % (coin['symbol']))

    def market_value(self, symbol, kline_size, date_s, date_f=""):
        date_s = datetime.strptime(date_s, "%d/%m/%Y %H:%M:%S")

        if date_f != "":
            date_f = datetime.strptime(date_f, "%d/%m/%Y %H:%M:%S")
        else:
            date_f = date_s + timedelta(seconds=59)

        print('Retrieving values...\n')
        klines = self.client.get_klines(symbol, kline_size, int(date_s.timestamp() * 1000),
                                        int(date_f.timestamp() * 1000)).json()

        if len(klines) > 0:
            for kline in klines:
                print('[%s] Open: %s High: %s Low: %s Close: %s' % (
                    datetime.fromtimestamp(kline[0] / 1000), kline[1], kline[2], kline[3], kline[4]))

        return
