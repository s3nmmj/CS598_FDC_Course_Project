import pandera as pa
from pandera import Column, DataFrameSchema, Check

stocks_schema = DataFrameSchema(
    {
        "ticker": Column(str),
        "date": Column(pa.DateTime),
        "open": Column(float, Check.ge(0), nullable=True),
        "high": Column(float, Check.ge(0), nullable=True),
        "low": Column(float, Check.ge(0), nullable=True),
        "close": Column(float, Check.ge(0), nullable=True),
        "adj_close": Column(float, Check.ge(0), nullable=True),
        "volume": Column(float, Check.ge(0), nullable=True),
        "ret_1d": Column(float, nullable=True),
        "rv_close_close_1d": Column(float, nullable=True),
        "rv_close_close_5d": Column(float, nullable=True),
        "rv_close_close_20d": Column(float, nullable=True),
        "rv_parkinson_5d": Column(float, nullable=True),
        "rv_parkinson_20d": Column(float, nullable=True),
    },
    index=pa.Index(pa.DateTime, coerce=True, name="date", nullable=False),
    coerce=True,
)

macro_schema = DataFrameSchema(
    {
        "date": Column(pa.DateTime),
        "CPI_U": Column(float, nullable=True),
        "UNRATE": Column(float, nullable=True),
        "FEDFUNDS": Column(float, nullable=True),
    },
    index=pa.Index(pa.DateTime, coerce=True, name="date", nullable=False),
    coerce=True,
)

integrated_schema = DataFrameSchema(
    {
        "ticker": Column(str),
        "date": Column(pa.DateTime),
        "ret_1d": Column(float, nullable=True),
        "rv_close_close_1d": Column(float, nullable=True),
        "rv_close_close_5d": Column(float, nullable=True),
        "rv_close_close_20d": Column(float, nullable=True),
        "rv_parkinson_5d": Column(float, nullable=True),
        "rv_parkinson_20d": Column(float, nullable=True),
        "CPI_U": Column(float, nullable=True),
        "UNRATE": Column(float, nullable=True),
        "FEDFUNDS": Column(float, nullable=True),
    },
    index=pa.Index(pa.DateTime, coerce=True, name="date", nullable=False),
    coerce=True,
)
