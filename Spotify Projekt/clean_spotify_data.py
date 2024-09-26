import pandas as pd

#spotify_dataframe  = pd.read_csv('dataset.csv')
#print(spotify_dataframe.columns)
#print(spotify_dataframe.head())
#print(spotify_dataframe.describe())
#print(spotify_dataframe.info())

#spotify_dataframe_cleaned = spotify_dataframe.drop(axis= 1, columns =['Unnamed: 0', 'track_id',
#       'popularity', 'duration_ms', 'explicit', 'danceability', 'energy',
#       'key', 'loudness', 'mode', 'speechiness', 'acousticness',
#       'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'])
#print(spotify_dataframe_cleaned.columns)
#print(spotify_dataframe_cleaned.shape)
#spotify_dataframe_cleaned.to_csv('spotify_dataframe_cleaned.csv' ,index = False ,  index_label= ['artists', 'album_name', 'track_name', 'track_genre'])

df = pd.read_csv('spotify_dataframe_cleaned.csv')
print(df.columns)







