from helpers import get_pe_ratio
import yfinance as yf

# Standards from "The Intelligent Investor" by Benjamin Graham
target_debt_to_equity = 0.5
target_pe_times_pb = 22.5

# Formats ticker and catches errors when analyzing a company
def analyze_ticker(ticker_symbol):
    try:
        return analyze_company(yf.Ticker(ticker_symbol))
    except Exception as error:
        print(f"Error analyzing {ticker_symbol}: {error}")
        return None

# performs calculations to determine if a company meets Graham's criteria
# returns the company name if it meets the criteria, otherwise returns None
def analyze_company(ticker):
    company_name = ticker.info["shortName"]
    debt_to_equity = ticker.info["debtToEquity"]
    price_to_book = ticker.info["priceToBook"]
    
    if debt_to_equity is None or price_to_book is None:
        return None
    debt_to_equity /= 100 # from percentage to decimal
    
    pe_ratio = get_pe_ratio(ticker)
    if pe_ratio is None:
        return None
    
    print(f"Analyzing {company_name}")

    if (
        0 <= debt_to_equity < target_debt_to_equity
        and pe_ratio > 0
        and price_to_book > 0
        and pe_ratio * price_to_book <= target_pe_times_pb
    ):
        return company_name

    return None
