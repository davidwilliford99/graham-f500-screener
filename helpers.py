import pandas as pd
import requests
from io import StringIO

# Return all tickers in Fortune 500 list from Wikipedia
def get_fortune_500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))
    sp500_df = tables[0] # The first table on the page contains the S&P 500 companies

    return sp500_df["Symbol"].str.replace(".", "-", regex=False).tolist()

# get the P/E ratio for the last 3 years
def get_pe_ratio(ticker):
    income = ticker.get_income_stmt(freq="yearly")
    eps = income.loc["DilutedEPS"].iloc[:3]
    avg_eps = eps.mean()
    price = ticker.info["currentPrice"]
    last_3y_pe_ratio = price / avg_eps
    return last_3y_pe_ratio