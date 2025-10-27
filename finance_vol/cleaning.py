import numpy as np
import pandas as pd


def clean_prices(df):
    df = df.copy()

    # Ensure numeric types
    for col in ["open", "high", "low", "close", "adj_close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["ticker"] = df["ticker"].astype(str)

    # Reset index so "date" becomes a column
    df = df.reset_index()

    # Drop duplicates based on date + ticker
    df = df.drop_duplicates(subset=["date", "ticker"])

    # Set back to datetime index
    df = df.set_index("date").sort_index()

    return df


def compute_volatility_features(df):
    frames = []
    for t, g in df.groupby("ticker"):
        g = g.sort_index()

        # 1-day log returns
        g["ret_1d"] = np.log(g["adj_close"] / g["adj_close"].shift(1))

        # Close-to-close volatility
        for k in (1, 5, 20):
            if k == 1:
                g[f"rv_close_close_{k}d"] = np.sqrt(252) * g["ret_1d"].abs()
            else:
                g[f"rv_close_close_{k}d"] = np.sqrt(252) * g["ret_1d"].rolling(k).std()

        # Parkinson volatility (uses high-low range)
        def parkinson(s_high, s_low, k):
            hl = (np.log(s_high / s_low)) ** 2
            return np.sqrt(252) * np.sqrt((1 / (4 * np.log(2))) * hl.rolling(k).mean())

        for k in (5, 20):
            g[f"rv_parkinson_{k}d"] = parkinson(g["high"], g["low"], k)

        frames.append(g)

    return pd.concat(frames)


def clean_macro(df):
    df = df.copy()

    # Ensure numeric
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Resample to daily frequency, forward fill missing values
    full = pd.DataFrame(index=pd.date_range(df.index.min(), df.index.max(), freq="D"))
    # Ensure index has name 'date' to satisfy schema expectations
    full.index.name = "date"
    return full.join(df, how="left").ffill()
