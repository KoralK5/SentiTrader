# perform sentiment analysis on the dataset

import re
import pandas as pd
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scraper import get_data

def clean_headline(headline):
    headline = re.sub("b[(')]", '', headline) # remove b'
    headline = re.sub('b[(")]', '', headline) # remove b"
    headline = re.sub("'", '', headline) # remove \'
    return headline

def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def get_polarity(text):
    return TextBlob(text).sentiment.polarity

def getSIA(text):
    sia = SentimentIntensityAnalyzer()
    sentiment= sia.polarity_scores(text)
    return sentiment

def prepare_data(days=14, rerun=True):
    if rerun:
        get_data()

    data = pd.read_csv("DJIA.csv")
    data2 = pd.read_csv("News.csv")

    combined_news = data2.groupby('Date')['News'].apply(lambda x: ' '.join(x)).reset_index()
    combined_news['News'] = combined_news['News'].apply(lambda x: clean_headline(x))

    combined_news['Subjectivity'] = combined_news['News'].apply(get_subjectivity)
    combined_news['Polarity'] = combined_news['News'].apply(get_polarity)

    compound = []
    neg = []
    pos = []
    neu = []
    SIA = 0
    for i in range (0, len(combined_news['News'])):
        SIA = getSIA(combined_news['News'][i])
        compound.append(SIA['compound'])
        neg.append(SIA['neg'])
        pos.append(SIA['pos'])
        neu.append(SIA['neu'])

    combined_news['compound'] = compound
    combined_news['neg'] = neg
    combined_news['pos'] = pos
    combined_news['neu'] = neu

    merged_data = pd.merge(combined_news, data, on='Date', how='inner')
    merged_data = merged_data.sort_values(by='Date', ascending=False)
    final_df = merged_data.head(days)
    final_df = final_df.drop(columns=['News'])

    final_df.to_csv('Data.csv', index=False)

if __name__ == '__main__':
    prepare_data()
    print('Done!')

