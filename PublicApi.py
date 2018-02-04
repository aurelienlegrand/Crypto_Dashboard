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

def get_currencies_data(currencies_list):
        colors = ["#8e5ea2", "#3e95cd", "#3cba9f", "#c45850", "#e8c3b9"]

        # Currently displaying data on the last 30 days
        days = 30
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        times = []
        times.append(start_date.strftime('%Y/%m/%d'))
        for date in range(days + 1):
            times.append((start_date + timedelta(days=date)).strftime('%Y/%m/%d'))

        currencies_data = {}
        for i, curr in enumerate(currencies_list):
            get_currency_data(curr, currencies_data, colors[i % len(colors)], start_date, end_date)

        return times, currencies_data

def get_currency_data(currency, currencies_data, color, start_date, end_date):
    prices_json = get_average_prices(currency, start_date, end_date)
    prices = []
    for price in prices_json:
        prices.append(price['weightedAverage'])

    currencies_data[currency] = {}
    currencies_data[currency]['values'] = prices
    currencies_data[currency]['color'] = color
