from flask import Flask, render_template, request, jsonify
from Helper.DBinit import *
from Helper.Database import *
from Controller.OrdersApi import *
from Controller.BalanceApi import *
from Controller.TradeApi import *
from Controller.BotGetOrder import *
from Function.Orders import *
from datetime import timedelta, datetime

app = Flask(__name__)


#TEST FIRST
@app.route("/")
def hello():
    return "<h1 style='color:black'>BOT READY</h1>"


@app.route('/list-balances', methods=['GET', 'POST'])
def list_balances():
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = BalanceApi(key, secret,username)
    data = api.balances()
    return data


@app.route('/check-balance', methods=['GET', 'POST'])
def check_balance():
    asset = request.args.get("asset")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = BalanceApi(key, secret, username)
    data = api.balance(asset)
    return data


@app.route('/get-price', methods=['GET', 'POST'])
def get_price():
    symbol = request.args.get("symbol")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = OrdersApi(key, secret, username)
    data = api.get_price(symbol)
    return data


@app.route('/get-info', methods=['GET', 'POST'])
def get_info():
    symbol = request.args.get("symbol")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = OrdersApi(key, secret, username)
    data = api.get_info(symbol)
    return data


@app.route('/get-order', methods=['GET', 'POST'])
def get_order():
    symbol = request.args.get("symbol")
    order_id = request.args.get("order_id")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = OrdersApi(key, secret, username)
    data = api.get_order(symbol,order_id)
    return data


@app.route('/get-order-status', methods=['GET', 'POST'])
def get_order_status():
    symbol = request.args.get("symbol")
    order_id = request.args.get("order_id")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = OrdersApi(key, secret, username)
    data = api.get_order_status(symbol,order_id)
    return data


@app.route('/get-all-order-list', methods=['GET', 'POST'])
def get_all_order_list():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = OrdersApi(key, secret, username)
    data = api.get_all_order_list(start_time,end_time)
    return data


@app.route('/get-order-all', methods=['GET', 'POST'])
def get_order_all():
    symbol = request.args.get("symbol")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = OrdersApi(key, secret, username)
    data = api.get_order_all(symbol)
    return data


@app.route('/get-open-orders', methods=['GET', 'POST'])
def get_open_order():
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = OrdersApi(key, secret, username)
    data = api.get_open_orders()
    return data


@app.route('/get-all-order-market', methods=['GET', 'POST'])
def get_all_order_market():
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    api = OrdersApi(key, secret, username)
    data = api.get_all_order_market()
    return data


@app.route('/buy-limit', methods=['GET', 'POST'])
def buy_limit():
    symbol = request.args.get("symbol")
    quantity = request.args.get("quantity")
    buy_price = request.args.get("buy_price")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    ome_dict = {
        "api_key": key,
        "secret_key": secret,
        "username": username
    }
    api = TradeApi(ome_dict)
    data = api.buy_limit(symbol, quantity, buy_price)
    return data


@app.route('/sell-limit', methods=['GET', 'POST'])
def sell_limit():
    symbol = request.args.get("symbol")
    quantity = request.args.get("quantity")
    sell_price = request.args.get("sell_price")
    body = request.get_json(silent=True)
    key = body['key']
    secret = body['secret']
    username = body['username']
    ome_dict = {
        "api_key": key,
        "secret_key": secret,
        "username": username
    }
    api = TradeApi(ome_dict)
    data = api.sell_limit(symbol, quantity, sell_price)
    return data


@app.route('/running-bot', methods=['GET', 'POST'])
def running_bot():
    t = BotGetOrder()
    t.run("Fajar Soegi", "DOGEUSDT")
    return {
        "msg": "Berhasil",
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0')
