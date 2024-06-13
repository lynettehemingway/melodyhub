# Download the dataset from https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db?resource=download
# Change the following path to the path of the csv file you just downloaded


import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE

import warnings
warnings.filterwarnings('ignore')

tracks = pd.read_csv(r"C:\Users\Tanu\Downloads\SpotifyFeatures.csv\SpotifyFeatures.csv")
# print(tracks.head())
# print(tracks.shape)
# print(tracks.info())
# print(tracks.isnull().sum())

tracks = tracks.drop(['track_id'], axis = 1)

# print(tracks['track_name'].nunique(), tracks.shape)

tracks = tracks.sort_values(by=['popularity'], ascending=False)
tracks.drop_duplicates(subset=['track_name'], keep='first', inplace=True)

song_vectorizer = CountVectorizer()
song_vectorizer.fit(tracks['genre'])

tracks = tracks.sort_values(by=['popularity'], ascending=False).head(10000)

def get_similarities(song_name, data):
    # Getting vector for the input song.
    text_array1 = song_vectorizer.transform(data[data['track_name'] == song_name]['genre']).toarray()
    num_array1 = data[data['track_name'] == song_name].select_dtypes(include=np.number).to_numpy()

    # We will store similarity for each row of the dataset.
    sim = []
    for idx, row in data.iterrows():
        name = row['track_name']

        # Getting vector for current song.
        text_array2 = song_vectorizer.transform(data[data['track_name'] == name]['genre']).toarray()
        num_array2 = data[data['track_name'] == name].select_dtypes(include=np.number).to_numpy()

        # Calculating similarities for text as well as numeric features
        text_sim = cosine_similarity(text_array1, text_array2)[0][0]
        num_sim = cosine_similarity(num_array1, num_array2)[0][0]
        sim.append(text_sim + num_sim)

    return sim

def recommend_songs(song_name, data=tracks):
    # Base case
    if tracks[tracks['track_name'] == song_name].shape[0] == 0:
        print('This song is either not so popular or you\
    have entered invalid_name.\n Some songs you may like:\n')

        for song in data.sample(n=5)['track_name'].values:
            print(song)
        return

    data['similarity_factor'] = get_similarities(song_name, data)

    data.sort_values(by=['similarity_factor', 'popularity'],
                     ascending=[False, False],
                     inplace=True)

    # First song will be the input song itself as the similarity will be highest.
    print(data[['track_name', 'artist_name']][2:7])



recommend_songs('Hall of Fame')
