import pandas as pd

def preprocess_spotify_data(raw_data):
    """
    Preprocess Spotify API data into a usable format for ML.
    """
    processed_data = pd.DataFrame(raw_data)
    return processed_data[["danceability", "energy", "valence", "label"]]

def normalize_column(df, column_name):
    """
    Normalize a column in a DataFrame.
    """
    max_val = df[column_name].max()
    min_val = df[column_name].min()
    df[column_name] = (df[column_name] - min_val) / (max_val - min_val)
    return df

