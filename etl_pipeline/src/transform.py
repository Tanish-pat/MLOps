"""
    clean and preprocess the data.
"""

import pandas as pd
from logger import get_logger

logger = get_logger()

def transform_data(dataframes):
    """Cleans and transforms the extracted data."""
    for name, df in dataframes.items():
        # Handle missing values
        for column in df.columns:
            if df[column].isnull().any():
                if df[column].dtype == 'object':
                    # Fill with mode for categorical data and reassign the column
                    mode_value = df[column].mode()[0]
                    df[column] = df[column].fillna(mode_value)
                else:
                    # Fill with mean for numerical data and reassign the column
                    mean_value = df[column].mean()
                    df[column] = df[column].fillna(mean_value)
        logger.info(f"Transformed data for {name}: filled missing values.")
        print(f"Transformed data for {name}: filled missing values.")
    return dataframes