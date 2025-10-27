# CS598 Course Project Pilot: End-to-End Data Curation Workflow: Stock Market Volatility & Macroeconomic Events: Data Curation Project

This repository contains code and documentation for an end-to-end data curation workflow that integrates U.S. stock market data with macroeconomic indicators.  
The goal is to create an analysis-ready dataset and support investigations into how macro events (e.g., inflation announcements, unemployment reports, interest-rate changes) influence sector ETF volatility.

---

## Features
- Automated acquisition of **daily OHLCV stock prices** from Yahoo Finance (via `yfinance`).
- Acquisition of **macro indicators** from FRED (CPI, Unemployment, Fed Funds).
- Cleaning and transformation of raw data (deduplication, type coercion, engineered volatility features).
- Integration of stock and macro datasets into a unified **analysis-ready dataset**.
- Schema validation using **Pandera** to enforce consistency.
- Provenance logging: JSON record with run timestamp, code version, parameters, and library versions.
- Outputs in **Parquet** and **CSV** formats for analysis and reproducibility.

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/s3nmmj/CS598_FDC_Course_Project.git
   cd CS598_FDC_Course_Project
   ```

2. Create a Python environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Dependencies include:
   - pandas, numpy
   - yfinance
   - fredapi or pandas_datareader
   - pandera
   - python-dotenv

3. (Optional) To access FRED data, obtain an API key from [FRED](https://fred.stlouisfed.org/docs/api/fred/) and save it in a `.env` file:
   ```
   FRED_API_KEY=api_key
   ```

---

## Usage
Run the pipeline from the command line:

```bash
python main.py \
  --tickers SPY,QQQ,XLF \
  --start 2015-01-01 \
  --end 2025-01-01 \
  --outdir out
```

**Arguments:**
- `--tickers`: Comma-separated list of tickers (default: SPY, QQQ, and 11 S&P sector ETFs).
- `--start`: Start date (default: 2015-01-01).
- `--end`: End date (default: today).
- `--outdir`: Output directory for results (default: `./out`).

---

## Repository Structure
```
├── main.py                  # CLI entrypoint
├── acquisition.py           # Download stock + macro data
├── cleaning.py              # Cleaning and feature engineering
├── integration.py           # Join stock + macro data
├── schema_definitions.py    # Pandera schemas
├── io_utils.py              # Output writing + provenance
├── tests.py                 # Basic validation tests
├── progress_report.md       # Course milestone report
└── README.md                # Project documentation
```

---

## Outputs
After a run, outputs are organized as:
```
out/
  data_raw/
    stocks_raw.parquet
    macro_raw.parquet
  data_curated/
    stocks_clean.parquet
    macro_clean.parquet
    analysis_ready.parquet
    analysis_ready.csv
  metadata/
    provenance.json
```
