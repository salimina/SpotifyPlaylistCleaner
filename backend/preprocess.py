# from sklearn.preprocessing import MinMaxScaler
# import pandas as pd

# def preprocess_data(data):
#     df = pd.DataFrame(data)
#     numeric_features = ['danceability', 'energy', 'tempo', 'valence']
#     scaler = MinMaxScaler()
#     df[numeric_features] = scaler.fit_transform(df[numeric_features])
    
#     df['skip_rate'] = df['skips'] / (df['plays'] + 1)  # Avoid division by zero
#     df.fillna(0, inplace=True)  # Handle missing values
#     return df
