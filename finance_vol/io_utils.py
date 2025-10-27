import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
import sys
import pandas as pd


@dataclass
class ProvenanceRecord:
    run_timestamp_utc: str
    code_version: str
    libraries: dict
    parameters: dict

def _lib_versions():
    import pandas, numpy, yfinance, pandera
    return {
        "python": sys.version.split()[0],
        "pandas": pandas.__version__,
        "numpy": numpy.__version__,
        "yfinance": yfinance.__version__,
        "pandera": pandera.__version__,
    }

def write_outputs(df_raw_stocks, df_raw_macro, df_clean_stocks, df_clean_macro, df_integrated, outdir):
    raw_dir = Path(outdir) / "data_raw"
    curated_dir = Path(outdir) / "data_curated"
    meta_dir = Path(outdir) / "metadata"
    for d in [raw_dir, curated_dir, meta_dir]:
        d.mkdir(parents=True, exist_ok=True)

    df_raw_stocks.to_parquet(raw_dir / "stocks_raw.parquet")
    df_raw_macro.to_parquet(raw_dir / "macro_raw.parquet")
    df_clean_stocks.to_parquet(curated_dir / "stocks_clean.parquet")
    df_clean_macro.to_parquet(curated_dir / "macro_clean.parquet")
    df_integrated.to_parquet(curated_dir / "analysis_ready.parquet")
    df_integrated.to_csv(curated_dir / "analysis_ready.csv")

    prov = ProvenanceRecord(
        run_timestamp_utc=datetime.utcnow().isoformat(),
        code_version="v1.0.0",
        libraries=_lib_versions(),
        parameters={"tickers": str(df_clean_stocks["ticker"].unique().tolist())}
    )
    with open(meta_dir / "provenance.json", "w") as f:
        json.dump(asdict(prov), f, indent=2)
