from Helper.Api import *

import logging
import logging.handlers
import sys

formater_str = '%(asctime)s,%(msecs)d %(levelname)s %(name)s: %(message)s'
formatter = logging.Formatter(formater_str)
date_fmt = "%Y-%b-%d %H:%M:%S"

LOGGER_ENUM = {'debug': 'debug.log', 'trading': 'trades.log', 'errors': 'general.log'}
#LOGGER_FILE = LOGGER_ENUM['pre']
LOGGER_FILE = "binance-update-trade.log"
FORMAT = '%(asctime)-15s - %(levelname)s:  %(message)s'

logging.basicConfig(filename=LOGGER_FILE, filemode='a',
                    format=formater_str, datefmt=date_fmt,
                    level=logging.INFO)


class UpdateTrade:
    def __init__(self, option):
        print("options: {0}".format(option))
        self.option = option
        self.secret = self.option.get('secret_key')
        print("options: {0}".format(self.secret))
        self.key = self.option.get('api_key')
        self.client = Api(self.key, self.secret)
        self.order_id = self.option.get('orderid')

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
