import pandas as pd

# Load SMSSpamCollection.txt
smsspam_txt = pd.read_csv('SMSSpamCollection.txt', sep='\t', names=["label", "message"], header=None)

# Load sms_spam.csv
sms_spam_csv = pd.read_csv('sms_spam.csv')

# Check for consistent column names
sms_spam_csv = sms_spam_csv.rename(columns={"type": "label", "text": "message"})  # Adjust column names if necessary

# Combine the two datasets
combined_data = pd.concat([smsspam_txt, sms_spam_csv], ignore_index=True)

# Save to a single CSV file
output_path = 'combined_sms_spam.csv'
combined_data.to_csv(output_path, index=False)

print(f"Combined data saved to {output_path}")


# import pandas as pd

# def clean_dataset(filepath: str) -> pd.DataFrame:
#     """
#     Load and clean the SMS spam dataset.
#     Removes rows with missing or invalid values in 'label' or 'message'.

#     Parameters:
#         filepath (str): Path to the CSV file.

#     Returns:
#         pd.DataFrame: A cleaned DataFrame with valid rows only.
#     """
#     try:
#         # Load the dataset
#         print(f"Loading data from {filepath}...")
#         df = pd.read_csv(filepath, header=None, names=["label", "message"], index_col=None)

#         # Debug: Display initial data structure
#         print("Initial dataset loaded:")
#         print(df.head())
#         print(df.info())

#         # Remove rows with missing or invalid data
#         print("Cleaning the dataset...")
#         df = df.dropna(subset=["label", "message"])  # Drop rows where either column is NaN
#         df = df[df["label"].apply(lambda x: isinstance(x, str))]  # Keep only rows where 'label' is a string
#         df = df[df["message"].apply(lambda x: isinstance(x, str))]  # Keep only rows where 'message' is a string

#         # Debug: Display cleaned data structure
#         print("Cleaned dataset summary:")
#         print(df.info())
#         print(df.head())

#         return df

#     except Exception as e:
#         print(f"Error cleaning data: {e}")
#         return None

# # Example usage
# file_path = 'combined_sms_spam.csv'
# cleaned_data = clean_dataset(file_path)

# if cleaned_data is not None:
#     print(f"Cleaned dataset with {cleaned_data.shape[0]} rows and {cleaned_data.shape[1]} columns.")
# else:
#     print("Failed to clean the dataset.")
