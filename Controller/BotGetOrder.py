from Helper.Api import *
from Function.Orders import *
from Helper.Database import *
import sys
import time
import threading
import math
import logging
import logging.handlers
import datetime
from Function.Orders import Orders

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


class BotGetOrder:
    # Define static vars
    WAIT_BOT_GET_ORDER = 2  # seconds
    WAIT_TIME_BUY_SELL = 1  # seconds
    WAIT_TIME_CHECK_BUY_SELL = 0.2  # seconds
    WAIT_TIME_CHECK_SELL = 5  # seconds
    WAIT_TIME_STOP_LOSS = 20  # seconds

    def __init__(self):
        self.api_key = None
        self.secret_key = None
        self.symbol = None
        self.username = None
        self.debug = True
        self.loop = 0
        self.wait_time = 4
        self.logger = self.setup_logger(self.symbol, debug=self.debug)

    @staticmethod
    def setup_logger(symbol, debug=True):
        """Function setup as many loggers as you want"""
        # handler = logging.FileHandler(log_file)
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        logger = logging.getLogger(symbol)

        stout_handler = logging.StreamHandler(sys.stdout)
        if debug:
            logger.setLevel(logging.DEBUG)
            stout_handler.setLevel(logging.DEBUG)

        # handler = logging.handlers.SysLogHandler(address='/dev/log')
        # logger.addHandler(handler)
        stout_handler.setFormatter(formatter)
        logger.addHandler(stout_handler)
        return logger

    def sync_order(self, api_key , secret_key, symbol_an, username):
        try:
            self.api_key = api_key
            self.secret_key = secret_key
            self.username  = username
            self.symbol = symbol_an
            init = Database()
            # conn = init.connect().cursor()
            conn = init.connect()
            cur = conn.cursor()
            x = datetime.datetime.now()
            start_date = x.strftime("%d/%m/%Y %H:%M:%S")
            query = f"SELECT distinct(symbol) as symbol FROM {binance_orders_table} WHERE username = '{username}'"
            cur.execute(query)
            result = cur.fetchall()
            hitung_symbol = len(result)
            if hitung_symbol > 0:
                print(f"TOTAL symbol {hitung_symbol}")
                for symbol in result:
                    client = Api(self.api_key, self.secret_key)
                    order = client.query_order_all(symbol[0]).json()
                    print(f"Total {len(order)}")
                    for i, jo in enumerate(order):
                        number = str(i)
                        order_id = jo['orderId']
                        query = f"SELECT * FROM {binance_orders_table} WHERE username = '{username}' and order_id = '{order_id}'"
                        cur.execute(query)
                        result = cur.fetchall()
                        hitung = len(result)
                        if hitung == 0:
                            print(f"Tidak ada {i}")
                            insert_data = (f'INSERT INTO {binance_orders_table} ('
                                           f'order_id, orderListId, clientOrderId, '
                                           f'cummulativeQuoteQty, executedQty, origQty, '
                                           f'price, selfTradePreventionMode,side, '
                                            f'status,symbol,timeInForce, transactionTime, type, workingTime, created_date,'
                                           f'updated_date, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)')
                            valx = (jo['orderId'], jo['orderListId'], jo['clientOrderId'],
                                   jo['cummulativeQuoteQty'], jo['executedQty'], jo['origQty'],
                                   jo['price'], jo['selfTradePreventionMode'], jo['side'], jo['status'],
                                   jo['symbol'], jo['timeInForce'], start_date, jo['type'],  jo['workingTime'], start_date, start_date, username)
                            cur.execute(insert_data, valx)
                            conn.commit()

                        else:
                            print(f" ada {i}")
                            update_data = (f"UPDATE {binance_orders_table} SET "
                                           f"orderListId = %s and clientOrderId = %s and cummulativeQuoteQty = %s and "
                                           f"executedQty = %s and origQty = %s and price = %s and selfTradePreventionMode = %s and "
                                           f"side = %s and status = %s and symbol = %s and timeInForce = %s and "
                                           f"transactionTime = %s and type = %s and workingTime = %s and updated_date = %s where "
                                           f" order_id = %s and username = %s ")
                            val = (jo['orderListId'], jo['clientOrderId'],
                                   jo['cummulativeQuoteQty'], jo['executedQty'], jo['origQty'],
                                   jo['price'], jo['selfTradePreventionMode'], jo['side'],
                                   jo['status'], jo['symbol'], jo['timeInForce'], start_date,
                                   jo['type'], jo['workingTime'], start_date, jo['orderId'], username)
                            cur.execute(update_data, val)
                            conn.commit()
                    self.logger.info(f'KEY {api_key} AND SECRET {secret_key}')
                    time.sleep(self.WAIT_BOT_GET_ORDER)
                    return None
        except Exception as e:
            # print('bl: %s' % (e))
            self.logger.debug('SYNC ORDER error: %s' % e)
            time.sleep(self.WAIT_BOT_GET_ORDER)
            return None

    def order_client(self, symbol, username):
        try:
            init = Database()
            conn = init.connect()
            cur = conn.cursor()
            username_list = []
            search_order = "SELECT username FROM m_members ;"
            cur.execute(search_order)
            result = cur.fetchall()
            for username in result:
                username_list.append(username)
            sql = 'SELECT api_key, secret_key, username FROM m_credential WHERE username IN (%s)'
            in_p = ', '.join(list(map(lambda arg: "'%s'" % arg, username_list)))
            sql = sql % in_p
            cur.execute(sql)
            result = cur.fetchall()
            for (api_key, secret_key, u_name) in result:
                #username_list.append(username)
                # self.logger.info(f'KEY {api_key} AND SECRET {secret_key}')
                # time.sleep(self.WAIT_BOT_GET_ORDER)
                self.sync_order(api_key, secret_key, symbol, u_name)
            return None
        except Exception as e:
            # print('bl: %s' % (e))
            self.logger.debug('RUNNING GET DATA error: %s' % e)
            time.sleep(self.WAIT_BOT_GET_ORDER)
            return None

    def action(self, symbol, username):
        username = self.username
        self.order_client(symbol, username)

    def run(self, username, symbol):

        cycle = 0
        actions = []
        self.symbol = symbol
        self.username = username
        print('Auto Trading GET ORDER for Binance.com @ Fajar Soegi')
        print('\n')

        print('Started...')
        print('Trading Symbol: %s' % symbol)
        print('Stop-Loss Amount: %s' % self.username)
        while cycle <= self.loop:

            start_time = time.time()

            action_trader = threading.Thread(target=self.action, args=(symbol, username,))
            actions.append(action_trader)
            action_trader.start()

            end_time = time.time()

            if end_time - start_time < self.wait_time:

                time.sleep(self.wait_time - (end_time - start_time))

                # 0 = Unlimited loop
                if self.loop > 0:
                    cycle = cycle + 1
