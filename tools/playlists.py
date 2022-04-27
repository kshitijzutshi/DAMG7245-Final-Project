import spotipy
import config
import os
from spotipy.oauth2 import SpotifyOAuth

# Credentials
os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = config.SPOTIPY_REDIRECT_URI

# spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())
# Defining scope to read user playlist and write playlist to user
scope = 'user-library-read user-follow-read playlist-modify-private playlist-modify user-top-read'
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_artists_from_playlist(playlist_uri):
    '''
    :param playlist_uri: Playlist to analyse
    :return: A dictionary(artist uri : artist name) of all primary artists in a playlist.
    '''
    artists = {}
    playlist_tracks = spotify.playlist_tracks(playlist_id=playlist_uri)
    for song in playlist_tracks['items']:
        if song['track']:
            print(song['track']['artists'][0]['name'])
            artists[song['track']['artists'][0]['uri']] = song['track']['artists'][0]['name']
    return artists


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
