import sys
import argparse

from Controller.BotGetOrder import BotGetOrder

if __name__ == '__main__':
    # Set parser

    # Get start
    t = BotGetOrder()
    t.run("Fajar Soegi","DOGEUSDT")
