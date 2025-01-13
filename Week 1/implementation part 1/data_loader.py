import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, sep="\t", names=["label", "message"])
    df["Length"] = df["message"].apply(len)
    return df
