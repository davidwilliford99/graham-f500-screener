# Graham-Style Stock Screener

A small Python script that screens S&P 500 companies using a few simplified
value-investing rules inspired by Benjamin Graham's *The Intelligent Investor*.
It prints the names of companies that pass every rule.

## Screening rules

| Rule | Requirement |
| --- | --- |
| Debt-to-equity | At least `0`; below `0.5` normally, `1.0` for Utilities, Industrials, Real Estate, and Energy, or `2.0` for Financials |
| P/E × P/B | At most `22.5`, with positive P/E and P/B |

<br>

* The __P/E estimate__ uses the __current share price__ divided by __average diluted EPS__
from the 3 most recent reported annual periods. __P/B__ and __debt-to-equity__
are retrieved from Yahoo Finance. Companies with unavailable required data are
not included.
* Company data is fetched concurrently using ten worker threads and cached in
`f500data.csv` for eight hours. The cache includes company details and financial
metrics; __intrinsic value__ is currently a placeholder.
* These are simplified screening rules, not a complete application of Graham's
principles or investment advice. Verify financial data independently, for
example with company annual __(10-K)__ and quarterly __(10-Q)__ reports.

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
