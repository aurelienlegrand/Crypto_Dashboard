from configparser import ConfigParser
import requests
import hmac, hashlib
import urllib.parse
import time
import pprint


class ApiUser:
    def __init__(self, username, configFile='settings.cfg'):
        self.username = username
        self.configFile = configFile
        self.key = None
        self.secret = None
        self.my_currencies = None
        self.load_config()
        self.get_my_currencies()

    def load_config(self):
        if self.configFile:
            config = ConfigParser()
            config.read(self.configFile)
            self.key = config.get('Poloniex', 'API_KEY')
            self.secret = config.get('Poloniex', 'SECRET')

    def __api_execute_command(self, command):
        post_data = (('command', command), ('nonce', int(time.time() * 1000000)))
        # Encode post_data for HMAC
        post_data_bytes = urllib.parse.urlencode(post_data).encode('utf8')
        sign = hmac.new(self.secret.encode(), post_data_bytes, hashlib.sha512).hexdigest()

        headers = {'Key': self.key, 'Sign': sign}
        r = requests.post('https://poloniex.com/tradingApi', data=post_data, headers=headers)
        return r

    def get_currencies(self):
        r = self.__api_execute_command('returnBalances')
        return r.json()

    def get_my_currencies(self):
        """ Returns only currencies that you own. """

        currencies = self.get_currencies()
        my_currencies = {}

        if currencies:
            for curr in currencies:
                if float(currencies[curr]) > 0:
                    my_currencies[curr] = {}
                    my_currencies[curr]["owned"] = currencies[curr]

            self.my_currencies = my_currencies

    def update_prices(self, stocks):
        """ Updates BTC and USD values for user currencies. """

        for curr in self.my_currencies:
            if "BTC_" + curr in stocks:
                self.my_currencies[curr]["btc_value"] = float(stocks["BTC_" + curr]["highestBid"]) * float(self.my_currencies[curr]["owned"])
            else:
                self.my_currencies[curr]["btc_value"] = "Not found."
                
            if "USDT_" + curr in stocks:
                self.my_currencies[curr]["usdt_value"] = float(stocks["USDT_" + curr]["highestBid"]) * float(self.my_currencies[curr]["owned"])
            elif self.my_currencies[curr]["btc_value"] != "Not found.":
                self.my_currencies[curr]["usdt_value"] = float(self.my_currencies[curr]["btc_value"]) * float(stocks["USDT_BTC"]["highestBid"])
            else:
                self.my_currencies[curr]["usdt_value"] = "Not found."
