# .\venv\Scripts\Activate.ps1
# python -m pip freeze > requirements.txt

import yfinance as yf
from analyzer import analyze_company
from helpers import get_fortune_500_tickers

worthwhile_investments = []

fortune_500_tickers = get_fortune_500_tickers()

# analyze each company in the Fortune 500 list
for ticker_symbol in fortune_500_tickers:
    try:
        ticker = yf.Ticker(ticker_symbol)
        company_name = analyze_company(ticker)
        if company_name:
            worthwhile_investments.append(company_name)
    except Exception as e:
        # print(f"Error analyzing {ticker_symbol}: {e}") 
        continue
        
# output the Buffet/Graham worthy investments  
print("\nWorthwhile Investments (according to Benjamin Graham's criteria): \n")
for investment in worthwhile_investments:
    print(investment)