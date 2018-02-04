from flask  import Flask, render_template
import requests
import json
from datetime import datetime, timedelta

from ApiUser import ApiUser
from PublicApi import get_average_prices, get_currencies_data

app = Flask(__name__)
user = ApiUser('Aurelien')

# Routing

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # Gets all cryptocurrencies ticker value
    stocks = requests.get('https://poloniex.com/public?command=returnTicker').json()

    user.update_prices(stocks)

    return render_template('index.html', user=user, stocks=stocks, my_stocks=user.my_currencies)

@app.route('/graphs', methods=['GET'])
def graphs():
    # Gets the data we need to disply the charts
    times, currencies_data = get_currencies_data()

    return render_template('graphs.html', times=times, currencies_data=currencies_data)

# Main

if __name__ == "__main__":
    app.run()
