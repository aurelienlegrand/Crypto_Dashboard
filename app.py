from flask  import Flask, render_template
import requests
import json

app = Flask(__name__)

# Routing

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user = {'username': 'Aurelien'}
    stocks_fake = [
        {
            'name': 'BTC',
            'value': '12096'
        },
        {
            'name': 'ETH',
            'value': '1133'
        }
    ]

    # Gets all cryptocurrencies ticker value
    stocks = requests.get('https://poloniex.com/public?command=returnTicker').json()

    # TODO : Filter currencies

    return render_template('index.html', title='Home', user=user, stocks=stocks)

# Main

if __name__ == "__main__":
    app.run()
