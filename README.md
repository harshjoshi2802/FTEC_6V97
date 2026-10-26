# Portfolio Tracker

A small command-line portfolio tracker using Python's standard library. Data is
kept in memory and disappears when the program exits. Requires Python 3.10+.

## Setup and run

Open a terminal in this folder:

```sh
python -m venv .venv
```

Activate it on macOS/Linux:

```sh
source .venv/bin/activate
```

Or Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Then run:

```sh
python -m pip install -r requirements.txt
python -m tracker.main
```

There are no third-party dependencies. The menu supports adding assets, setting
prices, creating/selecting/deleting portfolios, depositing cash, buying, selling,
and viewing balances and gains. Choose 0 to quit. Ctrl+C and end-of-input also
exit cleanly. Logs go to `tracker.log` in the current directory.

## Package layout

- `tracker/__init__.py`: identifies the Python package.
- `tracker/models.py`: asset, position, portfolio, and trade data objects.
- `tracker/assets.py`: asset definitions and a separate current-price dictionary.
- `tracker/portfolios.py`: portfolio management and portfolio valuation.
- `tracker/trading.py`: deposits, shared cash, buys, sells, and average-cost accounting.
- `tracker/validation.py`: shared text, number, and whole-share validation.
- `tracker/errors.py`: application error hierarchy for specific rejected operations.
- `tracker/cli.py`: menu, prompts, display formatting, and expected error handling.
- `tracker/main.py`: logging configuration, startup, and outermost error handling.

## Design decisions

1. **Whole shares only.** Fractional shares are refused to keep quantity handling
   simple. Positive integral values such as `2` and `2.0` are accepted.
2. **Tickers ignore case.** Tickers are trimmed and converted to uppercase so
   `aapl` and `AAPL` cannot create duplicate assets.
3. **Fully sold positions are removed from the view.** This keeps the holdings
   screen focused on current investments. Trade records and realized gains stay
   attached to the portfolio until the portfolio is deleted.
4. **Missing current prices appear as "Not priced".** Those positions remain
   visible, but their market values and unrealized gains are unavailable. Totals
   include priced holdings only and are clearly marked incomplete. A missing
   price is never treated as zero.
5. **Users see input and business-rule errors.** Rejections are logged once at
   WARNING where the CLI handles them; successful changes are logged at INFO
   in their service. Unexpected errors receive a friendly message on screen
   and a full traceback in the log at the outermost level.

Portfolio names are trimmed but case-sensitive. Creating a portfolio does not
select it automatically. Buy/sell prices do not overwrite current market prices.
Money uses `Decimal`; display values are rounded to two decimal places while
calculations keep decimal precision. Zero remains valid for current prices and
sell prices. Domain objects use ordinary classes with constructors.

## Manual check

1. Add AAPL and create/select a portfolio.
2. Deposit $1,000. Buy 10 shares at $20, then 10 at $30.
3. Check cash is $500 and average cost is $25 for 20 shares.
4. Sell 5 shares at $40. Cash is $700 and realized gain is $75.
5. Set current price to $35. Market value is $525 and unrealized gain is $150.
6. Try a duplicate ticker, unknown ticker, negative deposit, text as a number,
   fractional shares, overselling, and buying without enough cash.
7. Try deleting a portfolio while it holds shares. Sell the remaining shares
   at $0, then delete it. Cash must stay unchanged by deletion.
8. Check a second portfolio has independent holdings and uses the same cash.

## Git and submission

This folder includes actual local Git commits made during generation, attributed
to OpenAI. They are not a record of student-authored work. The implementation is
on `feature/portfolio-tracker`; `main` contains the initial package setup.
This is an AI-generated reference implementation; the assignment's stated policy
prohibits submitting AI-written code.

No GitHub repository or pull request has been created. If using this project in an
AI-permitted context, create an empty remote repository, then:

```sh
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
git push -u origin feature/portfolio-tracker
```

The assignment requests a pull request from the feature branch into main, left
unmerged, the instructor `mab105120` added as a collaborator, and the PR URL
submitted on Teams. Those account actions must still be completed separately.
