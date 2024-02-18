from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
from dotenv import find_dotenv, load_dotenv
from os import environ as env

import ai
import scraper
import sentiment

ENV_FILE = find_dotenv()
load_dotenv(ENV_FILE)

API_KEY = env.get("ALPACA_KEY")
SECRET_KEY = env.get('ALPACA_SECRET')
client = TradingClient(API_KEY, SECRET_KEY, paper=True)

def prepare_data():
    scraper.get_data()
    sentiment.prepare_data()

def ai_trade():
    buy = ai.predict()
    print('Buying' if buy else 'Selling' + '100 shares of DIA')

    order_details = MarketOrderRequest(
        symbol = 'DIA',
        qty = 100,
        side = OrderSide.BUY if buy else OrderSide.Sell,
        time_in_force = TimeInForce.DAY
    )

    order = client.submit_order(order_data=order_details)

def get_status():
    assets = client.get_all_positions()
    positions = [(asset.symbol, asset.qty, asset.current_price) for asset in assets]

    print(positions)

if __name__ == '__main__':
    print('Preparing Data...')
    prepare_data()

    print('Placing Orders...')
    ai_trade()

    print('Getting Order Status...')
    get_status()

