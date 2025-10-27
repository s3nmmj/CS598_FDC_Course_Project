from .schema_definitions import integrated_schema

def integrate(stocks, macro):
    # Ensure index name is 'date'
    stocks = stocks.copy()
    macro = macro.copy()
    if stocks.index.name != "date":
        stocks.index.name = "date"
    if macro.index.name != "date":
        macro.index.name = "date"

    # Drop duplicated 'date' column in macro to avoid join conflict (stocks already has 'date' column)
    if "date" in macro.columns:
        macro = macro.drop(columns=["date"])

    merged = stocks.join(macro, how="left")

    # Ensure a 'date' column exists (some pipelines keep date only as index)
    merged["date"] = merged.index

    keep = [
        "ticker","date","ret_1d","rv_close_close_1d","rv_close_close_5d",
        "rv_close_close_20d","rv_parkinson_5d","rv_parkinson_20d",
        "CPI_U","UNRATE","FEDFUNDS"
    ]
    merged = merged[keep]
    integrated_schema.validate(merged, lazy=True)
    return merged
