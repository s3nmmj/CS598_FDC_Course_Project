# Data Dictionary

This data dictionary describes the schemas defined in `finance_vol/schema_definitions.py`.

---

## stocks_schema
| Column              | Type        | Description                                   | Nullable | Checks         |
|---------------------|------------|-----------------------------------------------|----------|---------------|
| ticker              | str        | Stock ticker symbol                           | No       |               |
| date                | DateTime   | Date of record                                | No       |               |
| open                | float      | Opening price                                 | Yes      | >= 0          |
| high                | float      | Highest price                                 | Yes      | >= 0          |
| low                 | float      | Lowest price                                  | Yes      | >= 0          |
| close               | float      | Closing price                                 | Yes      | >= 0          |
| adj_close           | float      | Adjusted closing price                        | Yes      | >= 0          |
| volume              | float      | Trading volume                                | Yes      | >= 0          |
| ret_1d              | float      | 1-day return                                  | Yes      |               |
| rv_close_close_1d   | float      | Realized volatility (close-close, 1 day)      | Yes      |               |
| rv_close_close_5d   | float      | Realized volatility (close-close, 5 days)     | Yes      |               |
| rv_close_close_20d  | float      | Realized volatility (close-close, 20 days)    | Yes      |               |
| rv_parkinson_5d     | float      | Realized volatility (Parkinson, 5 days)       | Yes      |               |
| rv_parkinson_20d    | float      | Realized volatility (Parkinson, 20 days)      | Yes      |               |

Index: date (DateTime, not nullable)

---

## macro_schema
| Column    | Type      | Description                       | Nullable |
|-----------|----------|-----------------------------------|----------|
| date      | DateTime | Date of record                    | No       |
| CPI_U     | float    | Consumer Price Index (Urban)      | Yes      |
| UNRATE    | float    | Unemployment Rate                 | Yes      |
| FEDFUNDS  | float    | Federal Funds Rate                | Yes      |

Index: date (DateTime, not nullable)

---

## integrated_schema
| Column              | Type      | Description                                   | Nullable |
|---------------------|----------|-----------------------------------------------|----------|
| ticker              | str      | Stock ticker symbol                           | No       |
| date                | DateTime | Date of record                                | No       |
| ret_1d              | float    | 1-day return                                  | Yes      |
| rv_close_close_1d   | float    | Realized volatility (close-close, 1 day)      | Yes      |
| rv_close_close_5d   | float    | Realized volatility (close-close, 5 days)     | Yes      |
| rv_close_close_20d  | float    | Realized volatility (close-close, 20 days)    | Yes      |
| rv_parkinson_5d     | float    | Realized volatility (Parkinson, 5 days)       | Yes      |
| rv_parkinson_20d    | float    | Realized volatility (Parkinson, 20 days)      | Yes      |
| CPI_U               | float    | Consumer Price Index (Urban)                  | Yes      |
| UNRATE              | float    | Unemployment Rate                             | Yes      |
| FEDFUNDS            | float    | Federal Funds Rate                            | Yes      |

Index: date (DateTime, not nullable)

---

**Note:** All schemas use Pandera for data validation. Nullable columns may contain missing values. Checks indicate additional constraints (e.g., non-negative values).
