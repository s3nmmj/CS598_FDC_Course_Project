import logging

logging.basicConfig(level=logging.INFO)

def run_subset_test(df_integrated, min_days=252):
    logging.info("Running subset test")
    if df_integrated.empty:
        raise AssertionError("Integrated dataset is empty")
    for col in ["CPI_U","UNRATE","FEDFUNDS"]:
        if df_integrated[col].isna().all():
            raise AssertionError(f"Macro column {col} is empty")
    logging.info("Subset test completed successfully")
