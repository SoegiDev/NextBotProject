import time
from dotenv import load_dotenv
import os
from datetime import timedelta, datetime
from Function.Balance import *
import json


choices_menu = '''
Please select input menu :
Enter 1> Set Key and Secret
Enter 2> Validation Key And Secret
Enter 3> List Balance
Enter 4> Check Balance
Enter 5> Print Orders
Enter 6> Server Status
Enter 7> Market Value Specific
Enter 8> Market Value Range
Enter 9> Exit'''
global key, secret
choice = 0
while True:
    print(choices_menu)
    choice = input("Your choice (Input number 1 to 3) ? ")
    try:
        choice = int(choice)
        if choice == 1:
            print('Enter KEY: (i.e. KEY)')
            key = input()
            if key is not None:
                print('ENTER SECRET: (i.e. SECRET) ')
                secret = input()
            if secret is not None:
                continue
        if choice == 2:
            if key == "" and secret == "":
                print("Key dan Secret Must Filled")
            else:
                print("Key dan Secret Successfully Insert")
            continue

        if choice == 3:
            if key == "" and secret == "":
                print("Key dan Secret Must Filled")
            else:
                m = Balance(key, secret)
                m.balances()
            continue

        if choice == 4:
            if key == "" and secret == "":
                print("Key dan Secret Must Filled")
            else:
                print('Masukkan Asset: (i.e. USDT) ')
                asset = input()
                m = Balance(key, secret)
                m.balance(asset)
            continue

        if choice == 5:
            if key == "" and secret == "":
                print("Key dan Secret Must Filled")
            else:
                print('Masukkan Market / Symbol: (i.e. DOGEUSDT) ')
                symbol = input()
                m = Balance(key, secret)
                m.orders(symbol)
            continue

        if choice == 6:
            if key == "" and secret == "":
                print("Key dan Secret Must Filled")
            else:
                m = Balance(key, secret)
                m.server_status()
            continue

        if choice == 7:
            print('Masukkan Market: (i.e. BTCUSDT)')
            symbol = input()
            print('Masukkan date/time: (dd/mm/yyyy hh:mm:ss)')
            date_s = input()
            m = Balance(key, secret)
            m.market_value(symbol, "1m", date_s)

        if choice == 8:
            print('Masukkan Market: (i.e. BTCUSDT)')
            symbol = input()
            print('Masukkan Start date/time: (dd/mm/yyyy hh:mm:ss)')
            date_s = input()
            print('Masukkan End date/time: (dd/mm/yyyy hh:mm:ss)')
            date_f = input()
            print('Masukkan interval as in exchange (i.e. 5m, 1d):')
            interval = input()
            m = Balance(key, secret)
            m.market_value(symbol, interval, date_s, date_f)

        if choice == 9:
            break

    except Exception as e:
        print(e)
        continue

print(choice)
