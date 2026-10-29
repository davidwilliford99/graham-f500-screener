# Graham-Style Stock Screener

A small Python script that screens S&P 500 companies using a few simplified
value-investing rules inspired by Benjamin Graham's *The Intelligent Investor*.
It prints the names of companies that pass every rule.

## Screening rules

| Rule | Requirement |
| --- | --- |
| Debt-to-equity | At least `0` and below `0.5` |
| P/E × P/B | At most `22.5`, with positive P/E and P/B |

The P/E estimate uses the current share price divided by average diluted EPS
from up to the three most recent reported annual periods. P/B and debt-to-equity
are retrieved from Yahoo Finance. Companies with unavailable required data are
not included.

These are simplified screening rules, not a complete application of Graham's
principles or investment advice. Verify financial data independently, for
example with company annual (10-K) and quarterly (10-Q) reports.

## Run

Requires Python and an internet connection. From the project folder, install
dependencies and run the screener:

```powershell
python -m pip install -r requirements.txt
python main.py
```

On Windows, you can instead run `.\run.bat`; it installs the requirements and
starts the screener.

## Data sources

- [S&P 500 companies list on Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
- [Yahoo Finance](https://finance.yahoo.com/) via the `yfinance` Python package
