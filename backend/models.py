# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LinearRegression
# from sklearn.cluster import KMeans
# import pickle


# def train_skip_model(data):
#     X = data[['danceability', 'energy', 'tempo', 'skip_rate']]
#     y = data['skip']
#     model = RandomForestClassifier()
#     model.fit(X, y)
#     return model

# def train_time_decay_model(data):
#     X = data[['days_since_last_played', 'play_count', 'energy']]
#     y = data['stop_likelihood']
#     model = LinearRegression()
#     model.fit(X, y)
#     return model

# def train_audio_clustering(data, n_clusters=3):
#     X = data[['danceability', 'tempo', 'energy', 'valence']]
#     model = KMeans(n_clusters=n_clusters)
#     model.fit(X)
#     return model


# with open('skip_model.pkl', 'wb') as f:
#     pickle.dump(model, f)
