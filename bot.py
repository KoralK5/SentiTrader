# bot but multiple trades over time

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from time import sleep
from datetime import datetime

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

def place_order(buy, shares=100):
    print('Buying' if buy else 'Shorting' + f' {shares} shares of DIA')

    order_details = MarketOrderRequest(
        symbol = 'DIA',
        qty = shares,
        side = OrderSide.BUY if buy else OrderSide.SELL,
        time_in_force = TimeInForce.DAY
    )

    order = client.submit_order(order_data=order_details)

def status():
    account = client.get_account()
    assets = client.get_all_positions()

    equity = float(account.equity)
    last_equity = float(account.last_equity)
    balance_change = equity - last_equity
    balance_change_p = balance_change/equity

    print('-------------------------')
    print("ACCOUNT")
    print(f"Current Balance: {equity:.2f}")
    print(f"Daily Balance Change: {balance_change:.2f} ({balance_change_p*100:.2f}%)")
    print()
    print("ASSETS")
    for position in assets:
        print(f"{position.symbol}: {position.market_value} ({position.qty} shares)")

    print('-------------------------\n')

trade_until = datetime(2024, 4, 1)  # end trades this day
sleep_amount = 5 * 60               # 5 minutes
long = -1                           # currently long (1) or short (0)
m = 5                               # 5 minute interval
n = 0.1                             # 10% invest
if __name__ == '__main__':
    today = datetime.today()
    while today < trade_until:
        # print status
        status()

        # check news
        prepare_data()
        long_pred = ai.predict()

        # make trade
        if long_pred != long:
            long = long_pred
            assets = client.get_all_positions()
            market_value = float(assets[0].market_value) / float(assets[0].qty)

            client.close_all_positions(True)

            account = client.get_account()
            equity = float(account.equity)
            trade_cash = equity * n

            trade_shares = trade_cash // market_value
            place_order(long, trade_shares)
        else:
            print("No Status Change") # sleep

        sleep(sleep_amount)

    client.close_all_positions(True)
