# .\venv\Scripts\Activate.ps1
# python -m pip freeze > requirements.txt

from analyzer import analyze_company
from helpers import get_fortune_500_tickers
from concurrent.futures import ThreadPoolExecutor


worthwhile_investments = []

fortune_500_tickers = get_fortune_500_tickers()

num_threads = 10

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    # analyze company returns 'None' for companies that don't meet the criteria
    worthwhile_investments = [
        company_name for company_name in executor.map(analyze_company, fortune_500_tickers)
        if company_name is not None        
    ]
        
# output the Buffet/Graham worthy investments  
print("\nWorthwhile Investments (according to Benjamin Graham's criteria): \n")
for investment in worthwhile_investments:
    print(investment)