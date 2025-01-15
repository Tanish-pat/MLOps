import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the SMS spam dataset, fixing multi-index issues, and add a 'Length' column.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: A cleaned DataFrame with 'label', 'message', and 'Length' columns.
    """
    try:
        # Load the dataset
        df = pd.read_csv(filepath, header=None, names=["label", "message"], index_col=None)

        # Drop rows where both label and message are NaN
        df = df.dropna(subset=["label", "message"])

        # Ensure label and message are of the correct type
        df["message"] = df["message"].astype(str)
        df["label"] = df["label"].astype(str)

        # Add a 'Length' column
        df["Length"] = df["message"].apply(len)

        # Return the cleaned DataFrame
        return df

    except Exception as e:
        print(f"Error loading or processing data: {e}")
        return None
