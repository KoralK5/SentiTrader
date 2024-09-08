# SentiTrader

SentiTrader is a high-frequency trading bot that utilizes sentiment analysis from news articles to make trading decisions. The bot scrapes r/worldnews and employs various machine learning models to predict stock market trends, testing its accuracy on an Alpaca paper trading account.

![image](https://github.com/user-attachments/assets/1cfc3f1c-a578-453d-a603-fd69c1fa39c0)

## Features
- Web scraping news articles from r/worldnews for sentiment analysis.
- Machine learning models (Random Forest, MLP, LDA) for predictive analysis.
- Integrated with Alpaca for live paper trading tests.
- Achieved approximately 12% annualized returns (currently in testing phase).

## Machine Learning Models
The machine learning models used for this project, including Random Forest, MLP, and LDA, were developed and tuned based on sentiment analysis data. You can view the full implementation of the ML models [here](https://www.kaggle.com/code/koralkulacoglu/sentiment-analysis-stock-prediction/notebook).

![image](https://github.com/user-attachments/assets/7aa160de-ba9a-4c7f-99d5-01cfe0244e69)

## Files
- `ai.py`: Contains AI model and trading logic.
- `bot.py`: Core trading bot implementation.
- `scraper.py`: Web scraping and data extraction.
- `sentiment.py`: Sentiment analysis implementation.
- `trader.py`: Bot control and trading strategy.

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/KoralK5/SentiTrader.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the bot:
   ```bash
   python bot.py
