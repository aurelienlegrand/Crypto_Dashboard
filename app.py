from flask  import Flask, render_template
import requests
import json

from ApiUser import ApiUser

app = Flask(__name__)

# Routing

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # Gets all cryptocurrencies ticker value
    stocks = requests.get('https://poloniex.com/public?command=returnTicker').json()

    user = ApiUser('Aurelien')
    user.update_prices(stocks)

    return render_template('index.html', title='Home', user=user, stocks=stocks, my_stocks=user.my_currencies)

# Main

if __name__ == "__main__":
    app.run()
