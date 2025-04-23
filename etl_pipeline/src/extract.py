"""
    extract data from CSV files.
"""

import pandas as pd
import os
from logger import get_logger

logger = get_logger()

def extract_data(data_folder="../data/raw"):
    """Extracts data from all CSV files in the specified folder."""
    dataframes = {}
    try:
        for file in os.listdir(data_folder):
            if file.endswith(".csv"):
                file_path = os.path.join(data_folder, file)
                df = pd.read_csv(file_path)
                dataframes[file[:-4]] = df  # Use filename without '.csv' as key
                logger.info(f"Extracted {len(df)} records from {file}.")
                print(f"Extracted {len(df)} records from {file}.")
    except Exception as e:
        logger.error(f"Error extracting data: {e}")
        print(f"Error extracting data: {e}")
    return dataframes