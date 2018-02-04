import requests
from datetime import datetime, timedelta

def get_average_prices(currency, start_date, end_date):
    """ Returns the average price per day for this currency between the two dates.
        start_date and end_date must be datetime objects """
    # Ex : https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1515163043&end=1517755043&period=86400
    # Period is in seconds. 86400 = 24 hours.
    params = (('command', 'returnChartData'), ('currencyPair', currency), ('start', int(start_date.timestamp())), ('end', int(end_date.timestamp())), ('period', '86400'))
    r = requests.post('https://poloniex.com/public', params=params)
    return r.json()

def get_currencies_data():
        colors = ["#8e5ea2", "#3e95cd", "#3cba9f", "#c45850", "#e8c3b9"]

        # Currently displaying data on the last 30 days
        days = 30
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        times = []
        times.append(start_date.strftime('%Y/%m/%d'))
        for date in range(days + 1):
            times.append((start_date + timedelta(days=date)).strftime('%Y/%m/%d'))

        prices_btc_json = get_average_prices('USDT_BTC', start_date, end_date)
        prices_btc = []
        for prices in prices_btc_json:
            prices_btc.append(prices['weightedAverage'])

        prices_eth_json = get_average_prices('USDT_ETH', start_date, end_date)
        prices_eth = []
        for prices in prices_eth_json:
            prices_eth.append(prices['weightedAverage'])

        currencies_data = {}
        currencies_data['USDT_BTC'] = {}
        currencies_data['USDT_BTC']['values'] = prices_btc
        currencies_data['USDT_BTC']['color'] = colors[0]
        currencies_data['USDT_ETH'] = {}
        currencies_data['USDT_ETH']['values'] = prices_eth
        currencies_data['USDT_ETH']['color'] = colors[1]

        return times, currencies_data
