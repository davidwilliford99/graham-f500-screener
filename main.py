# .\venv\Scripts\Activate.ps1
# python -m pip freeze > requirements.txt

import csv

from analyzer import analyze_company
from helpers import get_fortune_500_data
from concurrent.futures import ThreadPoolExecutor

worthwhile_investments = []

fortune_500_tickers = get_fortune_500_data()

num_threads = 10

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    # analyze company returns 'None' for companies that don't meet the criteria
    worthwhile_investments = [
        company for company in executor.map(analyze_company, fortune_500_tickers)
        if company is not None
    ]

# Replace the output CSV with the latest results.
output_csv = "output.csv"
headers = [
    "ticker",
    "company_name",
    "debt_to_equity",
    "price_to_book",
    "industry",
    "share_price",
    "pe_ratio",
    "earnings_per_share",
    "book_value_per_share",
    "intrinsic_value",
    "margin_of_safety"
]
with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(worthwhile_investments)

# Output the qualifying company names to the console.
print("\nWorthwhile Investments (according to Benjamin Graham's criteria):\n")
for investment in worthwhile_investments:
    print(investment["company_name"])