from flask  import Flask, render_template
import requests
import json

from ApiUser import ApiUser

app = Flask(__name__)

# Routing

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user = ApiUser('Aurelien')

    # Gets all cryptocurrencies ticker value
    stocks = requests.get('https://poloniex.com/public?command=returnTicker').json()

    # TODO : Filter currencies

    return render_template('index.html', title='Home', user=user, stocks=stocks, my_stocks=user.get_my_currencies())

# Main

if __name__ == "__main__":
    app.run()
