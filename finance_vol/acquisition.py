import os
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

try:
    from fredapi import Fred
    _HAS_FREDAPI = True
except ImportError:
    _HAS_FREDAPI = False

try:
    import pandas_datareader.data as pdr
    _HAS_PDR = True
except ImportError:
    _HAS_PDR = False


def fetch_yfinance_prices(tickers, start, end):
    """Fetch daily OHLCV data for one or more tickers from Yahoo Finance."""
    data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        auto_adjust=False,
        group_by="ticker",
        progress=False,
        threads=True,
    )

    frames = []

    if isinstance(data.columns, pd.MultiIndex):
        # Multiple tickers: iterate over first-level ticker symbols
        for t in tickers:
            if t not in data.columns.levels[0]:
                continue
            df_t = data[t].copy()
            df_t = df_t.rename(
                columns={
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                    "Adj Close": "adj_close",
                    "Volume": "volume",
                }
            )
            df_t["ticker"] = t
            frames.append(df_t)
    else:
        # Single ticker: rename directly
        df_t = data.copy()
        df_t = df_t.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            }
        )
        # If tickers is a list, take the first element
        df_t["ticker"] = tickers[0] if isinstance(tickers, (list, tuple)) else tickers
        frames.append(df_t)

    if not frames:
        raise RuntimeError("No data returned from Yahoo Finance. Check tickers/date range.")

    df = pd.concat(frames, axis=0)
    df.index.name = "date"
    return df.reset_index().set_index("date").sort_index()


def fetch_fred_series(start, end, series_map):
    """Fetch multiple FRED series as a wide DataFrame with date index."""
    out = {}
    for friendly, (sid, _) in series_map.items():
        if _HAS_FREDAPI and os.getenv("FRED_API_KEY"):
            fred = Fred(api_key=os.getenv("FRED_API_KEY"))
            s = fred.get_series(sid, observation_start=start, observation_end=end)
        elif _HAS_PDR:
            s = pdr.DataReader(sid, "fred", start, end).squeeze()
        else:
            raise RuntimeError("No FRED API access. Install fredapi or pandas_datareader.")
        s.index = pd.to_datetime(s.index)
        s.name = friendly
        out[friendly] = s
    return pd.concat(out.values(), axis=1).sort_index()
