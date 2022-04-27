import spotipy
import csv
import boto3
from datetime import datetime
import os
import pandas as pd
import pickle, gzip, urllib, json

from configfiles.playlists import spotify_playlists
# from tools.playlists import get_artists_from_playlist, get_audio_features
from decouple import Config
# import config
from spotipy.oauth2 import SpotifyOAuth


# spotipy_object = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())

# print(spotipy_object)

# Credentials
# os.environ["SPOTIPY_CLIENT_ID"] = Config.SPOTIPY_CLIENT_ID
# os.environ["SPOTIPY_CLIENT_SECRET"] = Config.SPOTIPY_CLIENT_SECRET
# os.environ['SPOTIPY_REDIRECT_URI'] = Config.SPOTIPY_REDIRECT_URI  # Needed for user authorization

from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')


# Defining scope to read user playlist and write playlist to user
scope = 'user-library-read user-follow-read playlist-modify-private playlist-modify user-top-read'
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

PLAYLIST = 'weekly_top50'

# get audio features from tracks in playlist
def get_audio_features(playlist_uri):
    '''
    :param playlist_uri: Playlist to analyse
    :return: A dictionary(track uri : audio features) of all tracks in a playlist.
    '''
    audio_features = {}
    playlist_tracks = spotify.playlist_tracks(playlist_id=playlist_uri)
    for song in playlist_tracks['items']:
        if song['track']:
            audio_features[song['track']['uri']] = spotify.audio_features(song['track']['uri'])
    return audio_features


def gather_data_local():
    # For every track we're looking for
    final_data_dictionary = {
        'track_name': [],
        'track_id': [],
        'danceability': [],
        'energy': [], 
        'key': [], 
        'loudness': [], 
        'mode': [], 
        'speechiness' : [],
        'acousticness' : [], 
        'instrumentalness' : [],
        'liveness' : [], 
        'valence' : [], 
        'tempo' : [], 
        'duration_ms' : [],
        'time_signature' : []
    }
    audio_features = get_audio_features(spotify_playlists()[PLAYLIST])
    # import json
    # with open('data.json', 'w') as f:
    #     json.dump(audio_features, f)
    # print(audio_features)
    with open("top10_weekly.csv", 'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        audio_features = get_audio_features(spotify_playlists()[PLAYLIST])
        for track in audio_features.keys():
            # trackname_res = spotify.tracks(audio_features[track][0]['id'])
            # print(trackname_res['tracks'][0])
            writer.writerow({
                'track_name': 'track_'+str(audio_features[track][0]['id']),
                'track_id': audio_features[track][0]['id'],
                'danceability': audio_features[track][0]['danceability'],
                'energy': audio_features[track][0]['energy'],
                'key': audio_features[track][0]['key'],
                'loudness': audio_features[track][0]['loudness'],
                'mode': audio_features[track][0]['mode'],
                'speechiness': audio_features[track][0]['speechiness'],
                'acousticness': audio_features[track][0]['acousticness'],
                'instrumentalness': audio_features[track][0]['instrumentalness'],
                'liveness': audio_features[track][0]['liveness'],
                'valence': audio_features[track][0]['valence'],
                'tempo': audio_features[track][0]['tempo'],
                'duration_ms': audio_features[track][0]['duration_ms'],
                'time_signature': audio_features[track][0]['time_signature']
                })

            final_data_dictionary['track_name'].append('track_'+str(audio_features[track][0]['id']))
            final_data_dictionary['track_id'].append(audio_features[track][0]['id'])
            final_data_dictionary['danceability'].append(audio_features[track][0]['danceability'])
            final_data_dictionary['energy'].append(audio_features[track][0]['energy'])
            final_data_dictionary['key'].append(audio_features[track][0]['key'])
            final_data_dictionary['loudness'].append(audio_features[track][0]['loudness'])
            final_data_dictionary['mode'].append(audio_features[track][0]['mode'])
            final_data_dictionary['speechiness'].append(audio_features[track][0]['speechiness'])
            final_data_dictionary['acousticness'].append(audio_features[track][0]['acousticness'])
            final_data_dictionary['instrumentalness'].append(audio_features[track][0]['instrumentalness'])
            final_data_dictionary['liveness'].append(audio_features[track][0]['liveness'])
            final_data_dictionary['valence'].append(audio_features[track][0]['valence'])
            final_data_dictionary['tempo'].append(audio_features[track][0]['tempo'])
            final_data_dictionary['duration_ms'].append(audio_features[track][0]['duration_ms'])
            final_data_dictionary['time_signature'].append(audio_features[track][0]['time_signature'])

    unscaled_df = pd.read_csv('top10_weekly.csv')
    feat_cols_user = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

    # scaled_data = scaler.transform(unscaled_df[feat_cols_user])
    loaded_scalar = pickle.load(open('./model/StdScaler.sav', 'rb'))
    scaled_data = loaded_scalar.transform(unscaled_df[feat_cols_user])
    scaled_df = pd.DataFrame(scaled_data)
    scaled_df.to_csv('top10_weekly_scaled.csv', index=False)

    return final_data_dictionary


def gather_data():
#     s3_client = boto3.client('s3')
    data_bucket_name='music-rec-data'
    # For every artist we're looking for
    with open("/tmp/top10_tracks.csv", 'w') as file:
        header = ['track_name','track_id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness','liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        audio_features = get_audio_features(spotify_playlists()[PLAYLIST])
        for track in audio_features.keys():
            writer.writerow({
                'track_name': 'track_'+str(audio_features[track][0]['id']),
                'track_id': audio_features[track][0]['id'],
                'danceability': audio_features[track][0]['danceability'],
                'energy': audio_features[track][0]['energy'],
                'key': audio_features[track][0]['key'],
                'loudness': audio_features[track][0]['loudness'],
                'mode': audio_features[track][0]['mode'],
                'speechiness': audio_features[track][0]['speechiness'],
                'acousticness': audio_features[track][0]['acousticness'],
                'instrumentalness': audio_features[track][0]['instrumentalness'],
                'liveness': audio_features[track][0]['liveness'],
                'valence': audio_features[track][0]['valence'],
                'tempo': audio_features[track][0]['tempo'],
                'duration_ms': audio_features[track][0]['duration_ms'],
                'time_signature': audio_features[track][0]['time_signature']
                })


            # artists_albums = spotipy_object.artist_albums(artist, album_type='album', limit=50)
            # # For all of their albums
            # for album in artists_albums['items']:
            #     if 'GB' in artists_albums['items'][0]['available_markets']:
            #         album_data = spotipy_object.album(album['uri'])
            #         # For every song in the album
            #         album_length_ms = 0
            #         for song in album_data['tracks']['items']:
            #             # TODO consider album popularity
            #             album_length_ms = song['duration_ms'] + album_length_ms
            #         writer.writerow({'Year Released': album_data['release_date'][:4],
            #                          'Album Length': album_length_ms,
            #                          'Album Name': album_data['name'],
            #                          'Artist': album_data['artists'][0]['name']})

    s3_resource = boto3.resource('s3')
    date = datetime.now()
    filename = f'{date.year}/{date.month}/{date.day}/top10_tracks.csv'
    response = s3_resource.Object(Bucket=data_bucket_name, Key=filename).upload_file("top10_tracks.csv")

    return response


def lambda_handler(event, context):
    gather_data()


if __name__ == '__main__':

    
    data = gather_data_local()
    




