import argparse
from finance_vol import acquisition, cleaning, integration, io_utils, tests
from finance_vol.schema_definitions import stocks_schema, macro_schema

FRED_SERIES = {
    "CPI_U": ("CPIAUCSL", "M"),
    "UNRATE": ("UNRATE", "M"),
    "FEDFUNDS": ("FEDFUNDS", "D"),
}


def main():
    parser = argparse.ArgumentParser(description="Stock Volatility & Macro Integration Project")
    parser.add_argument("--tickers", default="SPY,QQQ,XLF,XLK,XLE,XLV,XLY,XLP,XLI,XLRE,XLU,XLB",
                        help="Comma-separated list of tickers (default: all 11 S&P sector ETFs + SPY, QQQ)")
    parser.add_argument("--start", default="2015-01-01", help="Start date (default: 2015-01-01)")
    parser.add_argument("--end", default=None, help="End date (default: today)")
    parser.add_argument("--outdir", default="out", help="Output directory (default: ./out)")
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",")]

    # --- Data Acquisition ---
    print("[step] Fetching prices from Yahoo Finance...")
    df_raw_stocks = acquisition.fetch_yfinance_prices(tickers, args.start, args.end)

    print("[step] Fetching macro indicators from FRED...")
    df_raw_macro = acquisition.fetch_fred_series(args.start, args.end, FRED_SERIES)

    # --- Cleaning & Feature Engineering ---
    print("[step] Cleaning stock prices...")
    df_clean_stocks = cleaning.clean_prices(df_raw_stocks)
    df_clean_stocks = cleaning.compute_volatility_features(df_clean_stocks)

    # Ensure "date" is both index and column
    df_clean_stocks = df_clean_stocks.reset_index().set_index("date")
    df_clean_stocks["date"] = df_clean_stocks.index

    print("[step] Validating stock schema...")
    stocks_schema.validate(df_clean_stocks)

    print("[step] Cleaning macro data...")
    df_clean_macro = cleaning.clean_macro(df_raw_macro)

    # Ensure "date" is both index and column
    df_clean_macro["date"] = df_clean_macro.index

    print("[step] Validating macro schema...")
    macro_schema.validate(df_clean_macro)

    # --- Integration ---
    print("[step] Integrating stock & macro data...")
    df_integrated = integration.integrate(df_clean_stocks, df_clean_macro)

    # --- Outputs ---
    print("[step] Writing outputs...")
    io_utils.write_outputs(
        df_raw_stocks, df_raw_macro, df_clean_stocks, df_clean_macro, df_integrated, args.outdir
    )

    # --- Tests ---
    print("[step] Running subset tests...")
    tests.run_subset_test(df_integrated)

    print("[done] Pipeline complete. Outputs available in:", args.outdir)


if __name__ == "__main__":
    main()
