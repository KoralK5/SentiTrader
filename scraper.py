# get news and stock price data for a current day and save it in CSV files

import requests
from bs4 import BeautifulSoup
import praw
from datetime import datetime
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
load_dotenv(ENV_FILE)

# make sure to set these!
API_KEY = env.get("REDDIT_KEY")
SECRET_KEY = env.get('REDDIT_SECRET')

def djia_fetcher(period1, period2):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    url = f"https://finance.yahoo.com/quote/%5EDJI/history?period1={period1}&period2={period2}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
    except requests.exceptions.ConnectionError as e:
        print("Error Connecting:", e)
    except requests.exceptions.Timeout as e:
        print("Timeout Error:", e)
    except requests.exceptions.RequestException as e:
        print("Request exception: ", e)

    # Parsing & Organizing Data
    headings = []  # A container to hold headings in the table
    data = []     # A container to hold contents in the table
    soup = BeautifulSoup(page.content, "lxml")
    table = soup.table

    # Read in table headings
    table_head = table.find('thead')
    table_headrows = table_head.find_all('th')
    for row in table_headrows:
        col = row.text.strip()
        headings.append(col.replace('*', ''))

    # Read in body content
    table_body = table.find('tbody')
    table_bodyrows = table_body.find_all('tr')
    for row in table_bodyrows:
        cols = row.select('td span')
        cols = [col.get_text() for col in cols]
        data.append(cols)

    return headings, data

def news_fetcher():
    reddit = praw.Reddit(
        client_id=API_KEY,
        client_secret=SECRET_KEY,
        user_agent="Scraper 1.0 by /u/PrettyDish9678",
    )

    subreddit = reddit.subreddit("worldnews")
    top_posts = subreddit.top("month", limit=2000)

    return top_posts

def get_data(days=30):
    dt = datetime.today()
    endTime = int(dt.timestamp())
    startTime = int(dt.timestamp()) - 60*60*24*(days+5)

    titles, data = djia_fetcher(startTime, endTime)
    data = data[:days]

    df = pd.DataFrame(data, columns=titles)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df.loc[:, df.columns != 'Date'] = df.loc[:, df.columns != 'Date'].apply(lambda x: x.str.replace(',', '').astype(float))

    news = news_fetcher()

    titles2 = ['Date', 'News']
    data2 = []
    for i in news:
        date = datetime.utcfromtimestamp(i.created_utc).date()
        title = i.title
        data2.append([date, title])

    df2 = pd.DataFrame(data2, columns=titles2)

    df.to_csv('DJIA.csv', index=False)
    df2.to_csv('News.csv', index=False)

if __name__ == '__main__':
    get_data()
    print('Done!')
