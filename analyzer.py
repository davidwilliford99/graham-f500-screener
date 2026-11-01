from helpers import get_pe_ratio

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

def analyze_company(company):
    company_name = company["company_name"]
    debt_to_equity = company["debt_to_equity"]
    price_to_book = company["price_to_book"]
    pe_ratio = company["pe_ratio"]

    if debt_to_equity is None or price_to_book is None:
        return None

    debt_to_equity /= 100

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