from helpers import get_pe_ratio
import yfinance as yf

target_debt_to_equity = 0.5
target_debt_to_equity_utilities = 1.0
target_debt_to_equity_financials = 2.0
target_pe_times_pb = 22.5

capital_intensive_sectors = {
    "Utilities",
    "Industrials",
    "Real Estate",
    "Energy"
}

def analyze_company(company: dict[str, str]):
    ticker = yf.Ticker(company["ticker"])
    company_name = ticker.info.get("shortName", company["ticker"])
    debt_to_equity = ticker.info.get("debtToEquity")
    price_to_book = ticker.info.get("priceToBook")

    if debt_to_equity is None or price_to_book is None:
        return None

    debt_to_equity /= 100

    pe_ratio = get_pe_ratio(ticker)

    if pe_ratio is None:
        return None

    if company["industry"] == "Financials":
        max_debt_to_equity = target_debt_to_equity_financials
    elif company["industry"] in capital_intensive_sectors:
        max_debt_to_equity = target_debt_to_equity_utilities
    else:
        max_debt_to_equity = target_debt_to_equity

    print(f"Analyzing {company_name}")

    if (
        0 <= debt_to_equity < max_debt_to_equity
        and pe_ratio > 0
        and price_to_book > 0
        and pe_ratio * price_to_book <= target_pe_times_pb
    ):
        return company_name

    return None