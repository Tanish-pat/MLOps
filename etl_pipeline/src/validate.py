"""
    check data quality
"""

import pandas as pd
from logger import get_logger

logger = get_logger()

def validate_data(df):
    """Performs basic validation checks on the DataFrame."""
    required_columns = ["Loan_ID", "Credit_History", "LoanAmount"]

    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Missing required column: {col}")
            print(f"Missing required column: {col}")
            return False

    if df.isnull().sum().sum() > 0:
        logger.warning("Data contains missing values.")
        print("Data contains missing values.")

    if df.duplicated().sum() > 0:
        logger.warning("Data contains duplicate records.")
        print("Data contains duplicate records.")

    logger.info(f"Data validation passed. {len(df)} records ready for loading.")
    print(f"Data validation passed. {len(df)} records ready for loading.")
    return True
