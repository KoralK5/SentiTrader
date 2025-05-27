# SentiTrader

SentiTrader is a medium-frequency trading bot that utilizes sentiment analysis from news articles to make trading decisions. The bot scrapes data from r/worldnews and employs machine learning models to predict stock market trends, testing its accuracy on an Alpaca paper trading account.

## 🔍 Machine Learning Models

The core of SentiTrader relies on machine learning models trained on sentiment analysis data to predict market trends. Models used:

- **Random Forest**
- **Multilayer Perceptron (MLP)**
- **Linear Discriminant Analysis (LDA)**

These models were trained and evaluated using sentiment-labeled financial news data.

📘 **Full implementation available on [Kaggle](https://www.kaggle.com/code/koralkulacoglu/sentiment-analysis-stock-prediction/notebook)**

![ML Models](https://github.com/user-attachments/assets/7aa160de-ba9a-4c7f-99d5-01cfe0244e69)

## ✨ Features

- Web scraping news articles from **r/worldnews** for sentiment analysis.
- Predictive analysis powered by ML models.
- Integrated with **Alpaca** for live paper trading.
- Achieved approximately **12% annualized returns** (currently in testing phase).

![Trading Performance](https://github.com/user-attachments/assets/1cfc3f1c-a578-453d-a603-fd69c1fa39c0)

## 📂 Files

- `ai.py` – Contains AI model and trading logic.
- `bot.py` – Core trading bot implementation.
- `scraper.py` – Web scraping and data extraction.
- `sentiment.py` – Sentiment analysis logic.
- `trader.py` – Bot control and trading strategy.

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KoralK5/SentiTrader.git
