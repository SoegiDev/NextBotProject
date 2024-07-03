
from Helper.Api import *


class BalanceApi:

    def __init__(self, key, secret, username):
        self.username = username
        self.client = Api(key, secret)

    def balances(self):
        try:
            response = self.client.get_account().json()
            data = []
            if 'msg' in response:
                return Response.get_res(400, response['msg'], 1)
            for balance in response['balances']:
                if float(balance['locked']) > 0 or float(balance['free']) > 0:
                    data.append({"asset": balance['asset'], "free": balance['free']})
            return Response.get_res(200, data, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)

    def balance(self, asset):
        try:
            response = self.client.get_account().json()
            if 'msg' in response:
                return Response.get_res(400, response['msg'], 1)
            acc = {item['asset']: item for item in response['balances']}
            data = {"asset": asset, "free": acc[asset]['free']}
            return Response.get_res(200, data, 0)
        except Exception as e:
            return Response.get_res(400, 'get_order Exception: %s' % e, 1)