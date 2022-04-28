from bottle import route, run, request
import spotipy
from spotipy import oauth2

import os, sys
cwd = os.getcwd()
sys.path.insert(1, cwd)
import config
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

#from decouple import config

PORT_NUMBER = 8080
load_dotenv()



SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')

SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')




# Defining scope to read user playlist and write playlist to user

scope = 'user-library-read user-follow-read playlist-modify-private playlist-modify user-top-read'

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
# os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
# os.environ['SPOTIPY_REDIRECT_URI'] = config.SPOTIPY_REDIRECT_URI   
# SPOTIPY_CLIENT_ID = config.SPOTIPY_CLIENT_ID
# SPOTIPY_CLIENT_SECRET = config.SPOTIPY_CLIENT_SECRET
# SPOTIPY_REDIRECT_URI = config.SPOTIPY_REDIRECT_URI
# SCOPE = 'user-library-read'
# CACHE = '.spotipyoauthcache'

# sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)

@route('/')
def index():
    access_token = ""
    token_info = spotify.get_cached_token()
    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = spotify.parse_response_code(url)
        if 'localhost' not in code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            #token_info = sp_oauth.get_access_token(code, as_dict=True)
            #access_token = token_info['access_token']
            #print(token_info)
            access_token = spotify.get_access_token(code, as_dict=False)

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results
    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'target='_blank'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = spotify.get_authorize_url()
    return auth_url

print(spotify.get_authorize_url())
run(host='', port=8080)