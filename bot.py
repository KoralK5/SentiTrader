# bot but multiple trades over time

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from time import sleep
from datetime import datetime
import requests
from bs4 import BeautifulSoup

import ai
import scraper
import sentiment

ENV_FILE = find_dotenv()
load_dotenv(ENV_FILE)

API_KEY = env.get("ALPACA_KEY")
SECRET_KEY = env.get('ALPACA_SECRET')
client = TradingClient(API_KEY, SECRET_KEY, paper=True)

def get_real_time_price():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }
    url = "https://finance.yahoo.com/quote/%5EDJI"
    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
        return None
    except requests.exceptions.ConnectionError as e:
        print("Error Connecting:", e)
        return None
    except requests.exceptions.Timeout as e:
        print("Timeout Error:", e)
        return None
    except requests.exceptions.RequestException as e:
        print("Request exception: ", e)
        return None

    # Parsing & Organizing Data
    soup = BeautifulSoup(page.content, "html.parser")
    fin_streamer = soup.find("fin-streamer", {"data-symbol": "^DJI", "data-field": "regularMarketPrice"})
    if not fin_streamer:
        print("Real-time price element not found on the page.")
        return None

    real_time_price = fin_streamer.get("value")
    if real_time_price:
        return real_time_price
    else:
        print("Real-time price not found.")
        return None

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
n = 0.5                             # 50% invest
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
            # assets = client.get_all_positions()
            # market_value = float(assets[0].market_value) / float(assets[0].qty)
            market_value = float(get_real_time_price()) / 100

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
