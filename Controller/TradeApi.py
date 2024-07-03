from Helper.Api import *
from Function.Orders import *
from Helper.Database import *
import datetime
import logging
import logging.handlers
import sys

formater_str = '%(asctime)s,%(msecs)d %(levelname)s %(name)s: %(message)s'
formatter = logging.Formatter(formater_str)
date_fmt = "%Y-%b-%d %H:%M:%S"

LOGGER_ENUM = {'debug': 'debug.log', 'trading': 'trades.log', 'errors': 'general.log'}
#LOGGER_FILE = LOGGER_ENUM['pre']
LOGGER_FILE = "binance-trader.log"
FORMAT = '%(asctime)-15s - %(levelname)s:  %(message)s'

logging.basicConfig(filename=LOGGER_FILE, filemode='a',
                    format=formater_str, datefmt=date_fmt,
                    level=logging.INFO)


class TradeApi:
    # Define static vars
    WAIT_TIME_BUY_SELL = 1  # seconds
    WAIT_TIME_CHECK_BUY_SELL = 0.2  # seconds
    WAIT_TIME_CHECK_SELL = 5  # seconds
    WAIT_TIME_STOP_LOSS = 20  # seconds

    def __init__(self, option):
        print("options: {0}".format(option))
        self.option = option
        self.secret = self.option.get('secret_key')
        print("options: {0}".format(self.secret))
        self.key = self.option.get('api_key')
        self.username = self.option.get('username')
        self.client = Api(self.key, self.secret)
        self.order_id = self.option.get('orderid')
        self.quantity = self.option.get('quantity')
        self.wait_time = self.option.get('wait_time')
        self.stop_loss = self.option.get('stop_loss')

        self.increasing = self.option.get('increasing')
        self.decreasing = self.option.get('decreasing')

        self.order_id = 0
        self.order_data = None

        # BTC amount
        self.amount = self.option.get('amount')

        self.logger = self.setup_logger(self.option.get('symbol'), debug=self.option.get('debug'))

    @staticmethod
    def setup_logger(symbol, debug=True):
        """Function setup as many loggers as you want"""
        #handler = logging.FileHandler(log_file)
        #handler.setFormatter(formatter)
        #logger.addHandler(handler)
        logger = logging.getLogger(symbol)

        stout_handler = logging.StreamHandler(sys.stdout)
        if debug:
            logger.setLevel(logging.DEBUG)
            stout_handler.setLevel(logging.DEBUG)

        #handler = logging.handlers.SysLogHandler(address='/dev/log')
        #logger.addHandler(handler)
        stout_handler.setFormatter(formatter)
        logger.addHandler(stout_handler)
        return logger

    def buy_limit(self, symbol, quantity, buy_price):
        try:
            init = Database()
            # conn = init.connect().cursor()
            conn = init.connect()
            cur = conn.cursor()
            if symbol is None:
                return Response.get_res(400, "Symbol Not Filled", 1)
            if quantity is None:
                return Response.get_res(400, "Quantity Not Filled", 1)
            if buy_price is None:
                return Response.get_res(400, "Buy Price Not Filled", 1)
            buy_price = float(buy_price)
            quantity = float(quantity)
            jo = self.client.buy_limit(symbol, quantity, buy_price).json()
            if 'msg' in jo:
                return Response.get_res(400, jo['msg'], 1)
            # Buy order created.
            x = datetime.datetime.now()
            start_date = x.strftime("%d/%m/%Y %H:%M:%S")
            insert_data = (f'INSERT INTO {binance_orders_table} ('
                           f'order_id, orderListId, clientOrderId, '
                           f'cummulativeQuoteQty, executedQty, origQty, '
                           f'price, selfTradePreventionMode,side, '
                           f'status,symbol,timeInForce, transactionTime, type, workingTime, created_date,'
                           f'updated_date, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)')
            valx = (jo['orderId'], jo['orderListId'], jo['clientOrderId'],
                    jo['cummulativeQuoteQty'], jo['executedQty'], jo['origQty'],
                    jo['price'], jo['selfTradePreventionMode'], jo['side'], jo['status'],
                    jo['symbol'], jo['timeInForce'], start_date, jo['type'], jo['workingTime'], start_date, start_date,
                    self.username)
            cur.execute(insert_data, valx)
            conn.commit()
            return Response.get_res(200, jo, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def sell_limit(self, symbol, quantity, sell_price):
        try:
            init = Database()
            # conn = init.connect().cursor()
            conn = init.connect()
            cur = conn.cursor()
            if symbol is None:
                return Response.get_res(400, "Symbol Not Filled", 1)
            if quantity is None:
                return Response.get_res(400, "Quantity Not Filled", 1)
            if sell_price is None:
                return Response.get_res(400, "Sell Price Not Filled", 1)
            sell_price = float(sell_price)
            quantity = float(quantity)
            jo = self.client.sell_limit(symbol, quantity, sell_price).json()
            sell_id = jo['orderId']
            # Buy order created.
            x = datetime.datetime.now()
            start_date = x.strftime("%d/%m/%Y %H:%M:%S")
            insert_data = (f'INSERT INTO {binance_orders_table} ('
                           f'order_id, orderListId, clientOrderId, '
                           f'cummulativeQuoteQty, executedQty, origQty, '
                           f'price, selfTradePreventionMode,side, '
                           f'status,symbol,timeInForce, transactionTime, type, workingTime, created_date,'
                           f'updated_date, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)')
            valx = (jo['orderId'], jo['orderListId'], jo['clientOrderId'],
                    jo['cummulativeQuoteQty'], jo['executedQty'], jo['origQty'],
                    jo['price'], jo['selfTradePreventionMode'], jo['side'], jo['status'],
                    jo['symbol'], jo['timeInForce'], start_date, jo['type'], jo['workingTime'], start_date, start_date,
                    self.username)
            cur.execute(insert_data, valx)
            conn.commit()
            return Response.get_res(200, jo, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def cancel(self, symbol, orderId):
        init = Database()
        # conn = init.connect().cursor()
        conn = init.connect()
        cur = conn.cursor()
        # If order is not filled, cancel it.
        get_order = Orders(self.key, self.secret)
        check_order = get_order.get_order(symbol, orderId)

        if not check_order:
            self.order_id = 0
            self.order_data = None
            return Response.get_res(400, "Order Not Found", 1)

        if check_order['status'] == 'NEW' or check_order['status'] != 'CANCELLED':
            x = datetime.datetime.now()
            start_date = x.strftime("%d/%m/%Y %H:%M:%S")
            get_order = Orders(self.key, self.secret)
            get_order.cancel_order(symbol, orderId)
            sql = (f"UPDATE {binance_orders_table} SET status = 'CANCELLED' and updated_date = {start_date} WHERE "
                   f"order_id = {orderId}")
            cur.execute(sql)
            conn.commit()
            return Response.get_res(200, get_order, 0)
        if check_order['status'] == 'FILLED':
            return Response.get_res(400, "Order Already Filled", 1)
