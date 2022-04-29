import spotipy
import csv
import os
import base64
import pandas as pd
import pickle, gzip, urllib, json
from configfiles.playlists import spotify_playlists
from decouple import Config
import requests
from spotipy.oauth2 import SpotifyOAuth

## REF ##
# https://prettystatic.com/automate-the-spotify-api-with-python/

from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Spotify API endpoints
TOKEN_URL = 'https://accounts.spotify.com/api/token'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'
headers = {}
data = {}

# Encode as Base64
message = f"{SPOTIPY_CLIENT_ID}:{SPOTIPY_CLIENT_SECRET}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')

headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(TOKEN_URL, headers=headers, data=data)
print(r.json())

token = r.json()['access_token']

# Defining scope to read user playlist and write playlist to user
# scope = 'user-library-read user-follow-read playlist-modify-private playlist-modify user-top-read'
# spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

PLAYLIST = 'weekly_top50'

# get audio features from tracks in playlist
def get_audio_features(playlist_uri):
    '''
    :param playlist_uri: Playlist to analyse
    :return: A dictionary(track uri : audio features) of all tracks in a playlist.
    '''
    GET_PLAYLIST_TRACKS_ENDPOINT = f'https://api.spotify.com/v1/playlists/{playlist_uri}/tracks'
    headers = {
    "Authorization": "Bearer " + token
    }
    audio_features = {}
    playlist_tracks_res = requests.get(url=GET_PLAYLIST_TRACKS_ENDPOINT, headers=headers)
    playlist_tracks = playlist_tracks_res.json()
    # print(json.dumps(playlist_tracks_res.json(), indent=2))
    # with open('data.json', 'w') as f:
    #     json.dump(playlist_tracks_res.json(), f)
    for song in playlist_tracks['items']:
        if song['track']:
            track_uri = song['track']['id']
            GET_TRACK_FEATURES_ENDPOINT = f'https://api.spotify.com/v1/audio-features/{track_uri}'
            audio_features_res = requests.get(url=GET_TRACK_FEATURES_ENDPOINT, headers=headers)
            audio_features[song['track']['id']] = audio_features_res.json()
     
    # with open('audio_features.json', 'w') as f:
    #     json.dump(audio_features, f)
            # audio_features[song['track']['uri']] = spotify.audio_features(song['track']['uri'])
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
    # track_id_val = '5QO79kh1waicV47BqGRL3g'
    # GET_TRACK_NAME_ENDPOINT = f'https://api.spotify.com/v1/tracks/{track_id_val}'
    # headers = {
    # "Authorization": "Bearer " + token
    # }
    # track_name_res = requests.get(url=GET_TRACK_NAME_ENDPOINT, headers=headers)
    # track_name_res = track_name_res.json()
    # with open('track_name_res.json', 'w') as f:
    #     json.dump(track_name_res, f)
    with open("top50_weekly.csv", 'w', newline='') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        audio_features = get_audio_features(spotify_playlists()[PLAYLIST])
        for track in audio_features.keys():
            # trackname_res = spotify.tracks(audio_features[track][0]['id'])
            # print(trackname_res['tracks'][0])
            track_id_val = audio_features[track]['id']
            GET_TRACK_NAME_ENDPOINT = f'https://api.spotify.com/v1/tracks/{track_id_val}'
            headers = {
            "Authorization": "Bearer " + token
            }
            track_name_res = requests.get(url=GET_TRACK_NAME_ENDPOINT, headers=headers)
            track_name_res = track_name_res.json()
            # with open('track_name_res.json', 'w') as f:
            #   json.dump(track_name_res, f)
            writer.writerow({
                'track_name': track_name_res['name'],
                'track_id': audio_features[track]['id'],
                'danceability': audio_features[track]['danceability'],
                'energy': audio_features[track]['energy'],
                'key': audio_features[track]['key'],
                'loudness': audio_features[track]['loudness'],
                'mode': audio_features[track]['mode'],
                'speechiness': audio_features[track]['speechiness'],
                'acousticness': audio_features[track]['acousticness'],
                'instrumentalness': audio_features[track]['instrumentalness'],
                'liveness': audio_features[track]['liveness'],
                'valence': audio_features[track]['valence'],
                'tempo': audio_features[track]['tempo'],
                'duration_ms': audio_features[track]['duration_ms'],
                'time_signature': audio_features[track]['time_signature']
                })

            final_data_dictionary['track_name'].append(track_name_res['name'])
            final_data_dictionary['track_id'].append(audio_features[track]['id'])
            final_data_dictionary['danceability'].append(audio_features[track]['danceability'])
            final_data_dictionary['energy'].append(audio_features[track]['energy'])
            final_data_dictionary['key'].append(audio_features[track]['key'])
            final_data_dictionary['loudness'].append(audio_features[track]['loudness'])
            final_data_dictionary['mode'].append(audio_features[track]['mode'])
            final_data_dictionary['speechiness'].append(audio_features[track]['speechiness'])
            final_data_dictionary['acousticness'].append(audio_features[track]['acousticness'])
            final_data_dictionary['instrumentalness'].append(audio_features[track]['instrumentalness'])
            final_data_dictionary['liveness'].append(audio_features[track]['liveness'])
            final_data_dictionary['valence'].append(audio_features[track]['valence'])
            final_data_dictionary['tempo'].append(audio_features[track]['tempo'])
            final_data_dictionary['duration_ms'].append(audio_features[track]['duration_ms'])
            final_data_dictionary['time_signature'].append(audio_features[track]['time_signature'])

    unscaled_df = pd.read_csv(f'top50_weekly.csv', encoding='unicode_escape')
    feat_cols_user = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

    # scaled_data = scaler.transform(unscaled_df[feat_cols_user])
    loaded_scalar = pickle.load(open('./model/StdScaler.sav', 'rb'))
    scaled_data = loaded_scalar.transform(unscaled_df[feat_cols_user])
    scaled_df = pd.DataFrame(scaled_data)
    scaled_df.to_csv('top10_weekly_scaled.csv', index=False)

    return final_data_dictionary


# def gather_data():
# #     s3_client = boto3.client('s3')
#     data_bucket_name='music-rec-data'
#     # For every artist we're looking for
#     with open("/tmp/top10_tracks.csv", 'w') as file:
#         header = ['track_name','track_id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness','liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

#         writer = csv.DictWriter(file, fieldnames=header)
#         writer.writeheader()
#         audio_features = get_audio_features(spotify_playlists()[PLAYLIST])
#         for track in audio_features.keys():
#             writer.writerow({
#                 'track_name': 'track_'+str(audio_features[track][0]['id']),
#                 'track_id': audio_features[track][0]['id'],
#                 'danceability': audio_features[track][0]['danceability'],
#                 'energy': audio_features[track][0]['energy'],
#                 'key': audio_features[track][0]['key'],
#                 'loudness': audio_features[track][0]['loudness'],
#                 'mode': audio_features[track][0]['mode'],
#                 'speechiness': audio_features[track][0]['speechiness'],
#                 'acousticness': audio_features[track][0]['acousticness'],
#                 'instrumentalness': audio_features[track][0]['instrumentalness'],
#                 'liveness': audio_features[track][0]['liveness'],
#                 'valence': audio_features[track][0]['valence'],
#                 'tempo': audio_features[track][0]['tempo'],
#                 'duration_ms': audio_features[track][0]['duration_ms'],
#                 'time_signature': audio_features[track][0]['time_signature']
#                 })


#             # artists_albums = spotipy_object.artist_albums(artist, album_type='album', limit=50)
#             # # For all of their albums
#             # for album in artists_albums['items']:
#             #     if 'GB' in artists_albums['items'][0]['available_markets']:
#             #         album_data = spotipy_object.album(album['uri'])
#             #         # For every song in the album
#             #         album_length_ms = 0
#             #         for song in album_data['tracks']['items']:
#             #             # TODO consider album popularity
#             #             album_length_ms = song['duration_ms'] + album_length_ms
#             #         writer.writerow({'Year Released': album_data['release_date'][:4],
#             #                          'Album Length': album_length_ms,
#             #                          'Album Name': album_data['name'],
#             #                          'Artist': album_data['artists'][0]['name']})

#     s3_resource = boto3.resource('s3')
#     date = datetime.now()
#     filename = f'{date.year}/{date.month}/{date.day}/top10_tracks.csv'
#     response = s3_resource.Object(Bucket=data_bucket_name, Key=filename).upload_file("top10_tracks.csv")

#     return response


# def lambda_handler(event, context):
#     gather_data()


if __name__ == '__main__':

    
    data = gather_data_local()
    




