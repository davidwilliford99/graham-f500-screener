from concurrent.futures import ThreadPoolExecutor
import os
import time
import pandas as pd
import requests
from io import StringIO
import yfinance as yf

# Return all relevvant fields in Fortune 500 table from Wikipedia
def get_fortune_500_data():
    
    print("Fetching Fortune 500 data from Wikipedia...")
    
    # create a csv file to cache the data (if non-existemt)
    csv_file = "f500data.csv"
    if not os.path.exists(csv_file):
        print(f"Creating {csv_file}...")
        open(csv_file, "w").close()
    
    # if the cached data is less than 8 hours old, use it
    last_modified_time = os.path.getmtime(csv_file)
    empty_file = os.path.getsize(csv_file) == 0
    if (time.time() - last_modified_time) < 28800 and not empty_file:
        print(f"Using cached data from {csv_file}...")
        return pd.read_csv("f500data.csv").to_dict(orient="records")

    # make a request to Wikipedia if data is not cached or is older than 8 hours
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text))
    sp500_df = tables[0] # The first table on the page contains the S&P 500 companies
    
    # extract the fields we want
    print("Extracting relevant fields from Fortune 500 data...")
    num_threads = 10
    
    # this thread iterates over the two columns of the dataframe
    # and passes them to the get_company_data function
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        f500data = list(
            executor.map(
                get_company_data,       # function to call for each company
                sp500_df["Symbol"],     # arg 1: ticker symbol
                sp500_df["GICS Sector"] # arg 2: industry
            )
        )
    
    print(f"Loading {len(f500data)} companies into CSV file.")
    pd.DataFrame(f500data).to_csv("f500data.csv", index=False) # cache to csv
    return f500data

# add all data fields we are interested in
# both from wikipedia and yfinance
def get_company_data(symbol, industry):
    print (f"Fetching data for {symbol}...")
    
    ticker_symbol = symbol.replace(".", "-")
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    return {
        "ticker": ticker_symbol,
        "company_name": info.get("shortName", symbol),
        "debt_to_equity": info.get("debtToEquity"),
        "price_to_book": info.get("priceToBook"),
        "industry": industry,
        "share_price": info.get("currentPrice"),
        "pe_ratio": get_pe_ratio(ticker, info),
        "intrinsic_value": None # to be calculated later
    }


# get the P/E ratio for the last 3 years
def get_pe_ratio(ticker, info):
    income = ticker.get_income_stmt(freq="yearly")
    if "DilutedEPS" not in income.index:
        return None
    eps = income.loc["DilutedEPS"].iloc[:3]
    avg_eps = eps.mean()
    price = info["currentPrice"]
    last_3y_pe_ratio = price / avg_eps
    return last_3y_pe_ratio