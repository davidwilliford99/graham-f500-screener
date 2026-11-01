import math

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

    calculate_intrinsic_value(company)
    calculate_margin_of_safety(company)

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
        return company

    return None


# return intrinsic value of a company based on Benjamin Graham's formula
# V = sqrt(22.5 * EPS * BVPS)
def calculate_intrinsic_value(company):
    if (
        company["earnings_per_share"] is None
        or company["book_value_per_share"] is None
        or company["earnings_per_share"] <= 0
        or company["book_value_per_share"] <= 0
    ):
        company["intrinsic_value"] = None
    else:
        company["intrinsic_value"] = math.sqrt(
            22.5 * company["earnings_per_share"] * company["book_value_per_share"]
        )

# % difference between intrinsic value and share price
def calculate_margin_of_safety(company):
    intrinsic_value = company.get("intrinsic_value")
    share_price = company.get("share_price")
    if intrinsic_value is None or intrinsic_value == 0 or share_price is None:
        company["margin_of_safety"] = None
    else:
        company["margin_of_safety"] = math.fabs((intrinsic_value - share_price) / intrinsic_value) * 100