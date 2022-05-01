import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import base64
import numpy as np
#from  PIL import ImageChops
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io 
import sqlite3 
import hashlib
import streamlit.components.v1 as components

from spotipy_client import *



# Get the current working directory
cwd = os.getcwd()


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


cols = ['Username', 'Password', 'Count', 'Timestamp']
lst = []
def add_userdata(username,password,count,time):
    lst.append([username,password,count,time])
    path = 'new.csv'

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
        df = pd.DataFrame(lst, columns = cols)
        df.to_csv("new.csv", index = False)
    else:
        df = pd.read_csv("new.csv")
        df = df.append(pd.DataFrame(lst, columns = cols), ignore_index=True)
        df.to_csv("new.csv", index = False)
    print(df)
    return df
    
# def add_userdata(username,password,count):
#     df = pd.dataframe(['username', 'password', count], columns = ['username', 'password', 'count'])
    
def login_user(username, password):
    a = pd.read_csv("new.csv")
    b = a.loc[(a['Username'] == username) & (a['Password'] == password)]
    print(b)
    c = b.to_numpy()
    return c

def view_all_users():
    a = pd.read_csv("new.csv")
    return a

def update_count(username):
    a = pd.read_csv("new.csv")
    cond = (a['Username'] == username)
    a.loc[cond,'Count'] = a['Count'] - 1
    a.to_csv("new.csv", index = False)
    
def read_count(username):
    a = pd.read_csv("new.csv")
    c =a.loc[a['Username'] == username, 'Count'].iloc[0]
    return c
#st.set_page_config(page_title="Sharone's Streamlit App Gallery", page_icon="", layout="wide")

# sysmenu = '''
# <style>
# #MainMenu {visibility:hidden;}
# footer {visibility:hidden;}
# '''
#st.markdown(sysmenu,unsafe_allow_html=True)

#Add a logo (optional) in the sidebar
# conn = sqlite3.connect('data.db')
# c = conn.cursor()
# # DB  Functions
# def create_usertable():
# 	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


# def add_userdata(username,password):
# 	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
# 	conn.commit()

# def login_user(username,password):
# 	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
# 	data = c.fetchall()
# 	return data


# def view_all_users():
# 	c.execute('SELECT * FROM userstable')
# 	data = c.fetchall()
# 	return data

# st.image(os.path.join(cwd, 'images', 'spotify_get_playlist_uri.png'))
# logo = Image.open(r'./assets/images/logo.png')
# profile = Image.open(r'./assets/images/twitter-logo.png')
# spotify = Image.open(r'./assets/images/spotify.png')
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'home'
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'output' not in st.session_state:
    st.session_state.output = 'Start Logging'
if 'got_rec' not in st.session_state:
    st.session_state.got_rec = False
if 'rec_type' not in st.session_state:
    st.session_state.rec_type = 'playlist'
if 'song_rec_type' not in st.session_state:
    st.session_state.rec_type = 'song'
if 'rec_uris' not in st.session_state:
    st.session_state.rec_uris = []
if 'rec_track_id' not in st.session_state:
    st.session_state.rec_track_id = 0

if 'user_op' not in st.session_state:
    st.session_state.user_op = 'Playlist'
def update_user_option():
    st.session_state.user_op = st.session_state.user_selection

if 'ml_model' not in st.session_state:
    st.session_state.ml_model = None

if 'login_success' not in st.session_state:
    st.session_state.login_success = False

if 'response_url' not in st.session_state:
    st.session_state.response_url = ''
def init_sp():
    st.session_state.spr.init_sp(st.session_state.response_url)

if 'example_url' not in st.session_state:
    st.session_state.example_url = 'Example: https://open.spotify.com/embed/playlist/37i9dQZF1DX0kbJZpiYdZl'
def update_playlist_url():
    st.session_state.example_url = st.session_state.playlist_url

if 'example_song_name' not in st.session_state:
    st.session_state.example_song_name = 'Example: Save your Tears'
def update_song_name():
    st.session_state.example_song_name = st.session_state.song_name

def add_feedback_df(feedback_df):
    feedback_db = User_FeedbackDB()
    feedback_db.add_feedback_df(feedback_df)
    del feedback_db
def convert_df():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    feedback_db = User_FeedbackDB()
    feedback_df = feedback_db.get_all_feedbacks_df()
    del feedback_db
    return feedback_df.to_csv().encode('utf-8')
if 'got_feedback' not in st.session_state:
    st.session_state.got_feedback = False
def add_feedback(feedback):
    rec_type = st.session_state.rec_type
    rec_name = st.session_state.rec_type
    username = ''
    ml_model_options = ''
    if st.session_state.rec_type != 'playlist':
        rec_type = 'favorite'
        username = st.session_state.username
    fb_list = [feedback, rec_type, rec_name, ml_model_options, username]
    feedback_db = User_FeedbackDB()
    feedback_db.add_user_feedback(fb_list)
    del feedback_db
    st.session_state.got_feedback = True

def playlist_page():
    st.subheader("User Playlist")
    st.markdown('---')
    playlist_uri = st.session_state.playlist_url.split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/playlist/' + playlist_uri
    components.iframe(uri_link, height=300)
    return
def song_name_page(song_uri):
    st.subheader("User's Song")
    st.markdown('---')
    # playlist_uri = st.session_state.playlist_url.split('/')[-1].split('?')[0]
    uri_link = 'https://embed.spotify.com/oembed/?url=spotify:track:' + song_uri
    components.iframe(uri_link, height=300)
    return

def get_recommendations(rec_type):
    st.session_state.got_rec = False
    st.session_state.got_feedback = False
    st.session_state.app_mode = 'recommend'
    st.session_state.rec_type = rec_type
def get_song_name_recommendations(rec_type):
    st.session_state.got_rec = False
    st.session_state.got_feedback = False
    st.session_state.app_mode = 'recommend'
    st.session_state.rec_type = rec_type

def insert_songs(placeholder, track_uris):
    with placeholder.container():
        for uri in track_uris:
            uri_link = "https://open.spotify.com/embed/track/" + uri + "?utm_source=generator&theme=0"
            components.iframe(uri_link, height=80)


def log_output(new_text):
    new_log = st.session_state.output
    if new_text != 'None':
        new_log = new_text + '\n' + st.session_state.output
    if st.session_state.display_output:
        st.session_state.output = st.session_state.log_holder.text_area('',value=new_log, height=500)

def load_spr_ml_model():
    st.session_state.ml_model = SPR_ML_Model()


def model_page():
    # st.subheader("Login")
	# 		# if password == '12345'
    # username = st.sidebar.text_input("User Name")
    # password = st.sidebar.text_input("User Password",type='password')
    # #count = 0
    # if st.sidebar.button("Login"):
    #     # if password == '12345':
    #     #create_usertable()
    #     hashed_pswd = make_hashes(password)
    #     result = login_user(username,check_hashes(password,hashed_pswd))
        
            
    #     if len(result):
    #         st.success("Logged In as {}".format(username))
    st.subheader("Select your preference")
    Types_of_Features = ("Playlist", "Song")
    st.session_state.user_selection = st.session_state.user_op
    st.radio("Feature", Types_of_Features, key='user_selection', on_change=update_user_option)

    if st.session_state.user_selection == "Playlist":
        st.session_state.playlist_url = st.session_state.example_url
        st.text_input("Playlist URI", key='playlist_url', on_change=update_playlist_url)
        playlist_uri = st.session_state.playlist_url.split('/')[-1]
        st.session_state.spr = SpotifyRecommendations(playlist_uri=playlist_uri)
        st.session_state.spr.log_output = log_output
        playlist_page()
        st.markdown("<br>", unsafe_allow_html=True)
        get_rec = st.button("Get Recommendations", key='pl', on_click=get_recommendations, args=('playlist',))
        
        if get_rec:
            if st.session_state.rec_type == 'playlist':
                st.subheader('Recommendations based on Playlist:')

            status_holder = st.empty()
            rec_songsholder = st.empty()
            user_fbholder = st.empty()

            left_column, middle_column, right_column = st.columns(3)
            with left_column:
                fb_plotholder = st.empty()
            with middle_column:
                playlist_wordcloud_holder = st.empty()
                user_cluster_all_holder = st.empty()
                
            with right_column:
                genre_wordcloud_holder = st.empty()
                user_cluster_single_holder = st.empty()
            if st.session_state.ml_model is None:
                with status_holder:
                    with st.spinner('Loading ML Model...'):
                        load_spr_ml_model()
                    st.success('ML Model Loaded!')
            else:
                log_output('ML model is already loaded')
            
            if st.session_state.got_rec == False:
                spr = st.session_state.spr
                spr.set_ml_model(st.session_state.ml_model)
                with status_holder:
                    with st.spinner('Getting Recommendations...'):
                        spr.len_of_favs = st.session_state.rec_type
                        spr.log_output = log_output
                        st.session_state.rec_uris = spr.get_songs_recommendations(n=10)
                        # st.session_state.genre_wordcloud_fig = spr.get_genre_wordcloud_fig()
                        # st.session_state.playlist_wordcloud_fig = spr.get_playlist_wordcloud_fig()
                        st.session_state.user_cluster_all_fig = spr.get_user_cluster_all_fig()
                        st.session_state.user_cluster_single_fig = spr.get_user_cluster_single_fig()
                        st.session_state.got_rec = True
                    st.success('Here are top 10 recommendations!')
            else:
                log_output('Showing already found recommendations')

            insert_songs(rec_songsholder, st.session_state.rec_uris)
    else:
        # first create a state for the text box update value

        st.session_state.song_name = st.session_state.example_song_name
        st.text_input("Song name", key='song_name', on_change=update_song_name)
        
        song_name = st.session_state.song_name
        # playlist_uri = st.session_state.playlist_url.split('/')[-1]
        st.session_state.spr = SpotifyRecommendations(song_name=song_name)
        load_spr_ml_model()
        spr = st.session_state.spr
        spr.set_ml_model(st.session_state.ml_model)
        track_uri = st.session_state.spr.get_track_uri_from_track_name()
        st.session_state.spr.log_output = log_output
        st.subheader("User's Song")
        st.markdown('---')
        uri_link = 'https://open.spotify.com/embed/track/' + track_uri
        components.iframe(uri_link, height=300)
        #song_name_page(track_uri)
        st.markdown("<br>", unsafe_allow_html=True)
        get_rec = st.button("Get Recommendations", key='song', on_click=get_song_name_recommendations, args=('song',))
        
        if get_rec:
            if st.session_state.rec_type == 'song':
                st.subheader('Recommendations based on Song:')

            status_holder = st.empty()
            rec_songsholder = st.empty()
            user_fbholder = st.empty()

            left_column, middle_column, right_column = st.columns(3)
            with left_column:
                fb_plotholder = st.empty()
            with middle_column:
                playlist_wordcloud_holder = st.empty()
                user_cluster_all_holder = st.empty()
                
            with right_column:
                genre_wordcloud_holder = st.empty()
                user_cluster_single_holder = st.empty()
            if st.session_state.ml_model is None:
                with status_holder:
                    with st.spinner('Loading ML Model...'):
                        load_spr_ml_model()
                    st.success('ML Model Loaded!')
            else:
                log_output('ML model is already loaded')
            
            if st.session_state.got_rec == False:
                spr = st.session_state.spr
                spr.set_ml_model(st.session_state.ml_model)
                with status_holder:
                    with st.spinner('Getting Recommendations...'):
                        spr.len_of_favs = st.session_state.rec_type
                        spr.log_output = log_output
                        
                        st.session_state.rec_uris = spr.get_song_recommendation_from_song_name(n=10)
                        # st.session_state.genre_wordcloud_fig = spr.get_genre_wordcloud_fig()
                        # st.session_state.playlist_wordcloud_fig = spr.get_playlist_wordcloud_fig()
                        # st.session_state.user_cluster_all_fig = spr.get_user_cluster_all_fig()
                        # st.session_state.user_cluster_single_fig = spr.get_user_cluster_single_fig()
                        st.session_state.got_rec = True
                    st.success('Here are top 10 recommendations!')
            else:
                log_output('Showing already found recommendations')

            insert_songs(rec_songsholder, st.session_state.rec_uris)


        with st.expander("Here's how to find any Playlist URL in Spotify"):
            st.write(""" 
                - Search for Playlist on the Spotify app
                - Right Click on the Playlist you like
                - Click "Share"
                - Choose "Copy link to playlist"
            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.image('./assets/images/spotify_get_playlist_uri.png')
            # st.image('./assets/images/spotify_get_playlist_uri.png')
        # else:
        #     st.warning("Incorrect Username/Password")



def rec_page():
    if 'spr' not in st.session_state:
        st.error('Please select an option in User Input page')
        return
    
    if st.session_state.rec_type == 'playlist':
        st.subheader('Recommendations based on Playlist:')
    elif st.session_state.rec_type == 'last_month':
        st.subheader('Recommendations based on your Last Month Favorites:')
    elif st.session_state.rec_type == '6_months':
        st.subheader('Recommendations based on your Six Months Favorites:')
    else:
        st.subheader('Recommendations based on your All Time Favorites:')
    status_holder = st.empty()
    rec_songsholder = st.empty()
    user_fbholder = st.empty()

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        fb_plotholder = st.empty()
    with middle_column:
        playlist_wordcloud_holder = st.empty()
        user_cluster_all_holder = st.empty()
        
    with right_column:
        genre_wordcloud_holder = st.empty()
        user_cluster_single_holder = st.empty()
    if st.session_state.ml_model is None:
        with status_holder:
            with st.spinner('Loading ML Model...'):
                load_spr_ml_model()
            st.success('ML Model Loaded!')
    else:
        log_output('ML Model already loaded')
    
    if st.session_state.got_rec == False:
        spr = st.session_state.spr
        spr.set_ml_model(st.session_state.ml_model)
        with status_holder:
            with st.spinner('Getting Recommendations...'):
                spr.len_of_favs = st.session_state.rec_type
                spr.log_output = log_output
                st.session_state.rec_uris = spr.get_songs_recommendations(n=10)
                # st.session_state.genre_wordcloud_fig = spr.get_genre_wordcloud_fig()
                # st.session_state.playlist_wordcloud_fig = spr.get_playlist_wordcloud_fig()
                st.session_state.user_cluster_all_fig = spr.get_user_cluster_all_fig()
                st.session_state.user_cluster_single_fig = spr.get_user_cluster_single_fig()
                st.session_state.got_rec = True
            st.success('Here are top 10 recommendations!')
    else:
        log_output('Showing already found recommendations')

    insert_songs(rec_songsholder, st.session_state.rec_uris)

    if st.session_state.got_feedback == False:
        with user_fbholder:
            c1, c2, c3, c4 = st.columns((1, 1, 1, 1))
            with c1:
                st.button("Love it", key='love', on_click=add_feedback, args=('Love it',))
            with c2:
                st.button("Like it", key='like', on_click=add_feedback, args=('Like it',))
            with c3:
                st.button("Okay", key='okay', on_click=add_feedback, args=('Okay',))
            with c4:
                st.button("Hate it", key='hate', on_click=add_feedback, args=('Hate it',))

    with fb_plotholder:
        try:
            feedback_db = User_FeedbackDB()
            fig = feedback_db.get_feedback_plot()
            del feedback_db
            if fig:
                st.subheader('User Feedback:')
                st.plotly_chart(fig, use_container_width=True)
        except:
            pass

    # genre_wordcloud_holder.pyplot(st.session_state.genre_wordcloud_fig)
    # playlist_wordcloud_holder.pyplot(st.session_state.playlist_wordcloud_fig)
    user_cluster_all_holder.pyplot(st.session_state.user_cluster_all_fig)
    user_cluster_single_holder.pyplot(st.session_state.user_cluster_single_fig)


#def spr_sidebar():
with st.sidebar:
    #model_button = st.button('Recommendation')
    #print(os.getcwd())
    print('./assets/images/spotify.png')
    st.image('./assets/images/spotify.png')
    choose = option_menu("Spotify Music Recommendation App", ["Home", "Dataset", "Model", "Recommendations", "Conclusions"],
                                icons=['house', 'file-earmark-music-fill', 'pc', 'boombox','journal'],
                                menu_icon="app-indicator", default_index=0,
                                styles={
                "container": {"padding": "5!important", "background-color": "#fafafa", "font": "proxima nova"},
                "icon": {"color": "#1DB954", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#181818"},
            }
            )
    st.checkbox('Display Output', True, key='display_output')
    st.session_state.log_holder = st.empty()
    log_output('None')

    # st.image(spotify, width=300)
    # st.subheader("Login")
	# # 		# if password == '12345'
    # username = st.text_input("User Name")
    # password = st.text_input("User Password",type='password')
    # # #count = 0
    # if st.sidebar.button("Login"):
    #     # if password == '12345':
    #     #create_usertable()
    #     hashed_pswd = make_hashes(password)
    #     result = login_user(username,check_hashes(password,hashed_pswd))
        
            
    #     if len(result):
            
    #         st.success("Logged In as {}".format(username))
    #         # choose = option_menu("Spotify Music Recommendation App", ["Home", "Dataset", "Model", "Recommendations", "Conclusions"],
    #         #                     icons=['house', 'file-earmark-music-fill', 'pc', 'boombox','journal'],
    #         #                     menu_icon="app-indicator", default_index=0,
    #         #                     styles={
    #         #     "container": {"padding": "5!important", "background-color": "#fafafa", "font": "proxima nova"},
    #         #     "icon": {"color": "#1DB954", "font-size": "25px"}, 
    #         #     "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    #         #     "nav-link-selected": {"background-color": "#181818"},
    #         # }
    #         # )
    #         st.checkbox('Display Output', True, key='display_output')
    #         st.session_state.log_holder = st.empty()
    #         log_output('None')

    #     else:
    #         st.warning("Incorrect Username/Password")

# if choose == "Recommendations":
#             st.session_state.app_mode = 'model'


# logo = Image.open(r'./assets/images/logo.png')
# profile = Image.open(r'./assets/images/twitter-logo.png')

# """### gif from local file"""
# file_ = open(r'./assets/images/login.gif', "rb")
# contents = file_.read()
# data_url = base64.b64encode(contents).decode("utf-8")
# file_.close()


st.title('Spotify Music Recommendation App')
# Home is where user will login
if choose == "Home":
    st.subheader("Login")
	# # 		# if password == '12345'
    username = st.text_input("User Name")
    password = st.text_input("User Password",type='password')
    if st.button("Login"):
            # if password == '12345':
            #create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))
            
                
            if len(result):
                
                st.success("Logged In as {}".format(username))
                st.session_state.login_success=True

				# task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				# if task == "Add Post":
				# 	st.subheader("Add Your Post")

				# elif task == "Analytics":
				# 	st.subheader("Analytics")
				# elif task == "Profiles":
				# 	st.subheader("User Profiles")
				# 	user_result = view_all_users()
				# 	clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
				# 	st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")

    elif st.checkbox("New User?"):
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
        #create_usertable()
            add_userdata(new_user,make_hashes(new_password), 10, datetime.datetime.now())
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


    
        

elif choose == "Dataset":
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ## Spotify Million Playlist Dataset
    -----------------------------------
    For this project we are using The Million Playist Dataset, as it name implies, the dataset consists of one million playlists and each playlists 
    contains n number of songs and some metadata is included as well such as name of the playlist, duration, number of songs, number of artists, etc.
    
    It is created by sampling playlists from the billions of playlists that Spotify users have created over the years. 
    Playlists that meet the following criteria were selected at random:
    - Created by a user that resides in the United States and is at least 13 years old
    - Was a public playlist at the time the MPD was generated
    - Contains at least 5 tracks
    - Contains no more than 250 tracks
    - Contains at least 3 unique artists
    - Contains at least 2 unique albums
    - Has no local tracks (local tracks are non-Spotify tracks that a user has on their local device
    - Has at least one follower (not including the creator
    - Was created after January 1, 2010 and before December 1, 2017
    - Does not have an offensive title
    - Does not have an adult-oriented title if the playlist was created by a user under 18 years of age
    
    As you can imagine a million anything is too large to handle and we are going to be using 2% of the data (20,000 playlists) to create the models 
    and then using it to train the model on AWS SageMaker and then use it to make predictions by exposing the model as a REST API Endpoint.
   
    ### Enhancing the data:
    Since this dataset is released by Spotify, it already includes a track id that can be used to generate API calls and 
    access the multiple information that is provided from Spotify for a given song, artist or user.
    These are some of the features that are available to us for each song and we are going to use them to enhance our dataset and to help matching 
    the user's favorite playlist.
    
    ##### Some of the available features are the following, they are measured mostly in a scale of 0-1:
    - **acousticness:** Confidence measure from 0.0 to 1.0 on if a track is acoustic.   
    - **danceability:** Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, 
    rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.   
    - **energy:** Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, 
    energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. 
    Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.   
    - **instrumentalness:** Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or 
    spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. 
    Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.   
    - **liveness:** Detects the presence of an audience in the recording. Higher liveness values represent an increased probability 
    that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.   
    - **loudness:** The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful 
    for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical 
    strength (amplitude). Values typical range between -60 and 0 db.   
    - **speechiness:** Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording 
    (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably 
    made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in 
    sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.   
    - **tempo:** The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the 
    speed or pace of a given piece and derives directly from the average beat duration.   
    - **valence:** A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound 
    more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).   
    
    Information about features: [link](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)
    """
    st.markdown("<br>", unsafe_allow_html=True)


elif choose == "Model":
    st.header('Spotify Playlist Recommender (SPR) Model')
    st.markdown('---')
    st.markdown("<br>", unsafe_allow_html=True)
    """
    For this project we used the Unsupervised learning model - K Means Clustering.
    The training and deployment of the K-Means Clustering algorithm was done using AWS SageMaker.  Amazon Sagemaker is a cloud machine learning platform that enables developers to build, train and deploy ML models quickly.
    For detailed walkthrough of the process, there is a Youtube video walkthrough created by us here - 
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.video('https://www.youtube.com/watch?v=_ZriVJjLF6Q&t=420s')


elif choose == "Recommendations":

    st.session_state.app_mode = 'model'
    if st.session_state.app_mode == 'model' and st.session_state.login_success:
        model_page()
    else:
        st.warning("Please Login to get Recommendations")
    # st.subheader("Login")
	# # 		# if password == '12345'
    # username = st.text_input("User Name")
    # password = st.text_input("User Password",type='password')
    # # #count = 0
    # if st.button("Login"):
    #     # if password == '12345':
    #     #create_usertable()
    #     hashed_pswd = make_hashes(password)
    #     result = login_user(username,check_hashes(password,hashed_pswd))
        
            
    #     if len(result):
    #         st.success("Logged In as {}".format(username))
    #         st.session_state.app_mode = 'model'
    #         if st.session_state.app_mode == 'model':
    #             model_page()

    #     else:
    #         st.warning("Incorrect Username/Password")
    #st.session_state.app_mode = 'recommend'
    # st.markdown(""" <style> .font {
    # font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    # </style> """, unsafe_allow_html=True)
    # st.markdown('<p class="font">Learn Python for Data Science</p>', unsafe_allow_html=True)

    # st.subheader('Import Data into Python')
    # st.markdown('To start a data science project in Python, you will need to first import your data into a Pandas data frame. Often times we have our raw data stored in a local folder in csv format. Therefore let\'s learn how to use Pandas\' read_csv method to read our sample data into Python.')

    # #Display the first code snippet
    # code = '''import pandas as pd #import the pandas library\ndf=pd.read_csv(r'C:\\Users\\13525\\Desktop\\ecourse_app\\ecourse_streamlit\\data.csv') #read the csv file into pandas\ndf.head() #display the first 5 rows of the data'''
    # st.code(code, language='python')

    # #Allow users to check the results of the first code snippet by clicking the 'Check Results' button
    # # df=pd.read_csv(r'C:\Users\13525\Desktop\ecourse_app\ecourse_streamlit\data.csv')
    # # df_head=df.head()
    # if st.button('Check Results', key='1'):
    #     st.write("Here's what the first 5 rows look like:")
    # else:
    #     st.write('---')

    # #Display the second code snippet
    # code = '''df.tail() #display the last 5 rows of the data'''
    # st.code(code, language='python')

    # #Allow users to check the results of the second code snippet by clicking the 'Check Results' button
    # # df=pd.read_csv(r'C:\Users\13525\Desktop\sample_data.csv')
    # # df_tail=df.tail()
    # if st.button('Check Results', key='2'):
    #     st.write("Here's what the last 5 rows look like1:")
    # else:
    #     st.write('---')     

    # #Display the third code snippet
    # st.write('   ')
    # st.markdown('After we import the data into Python, we can use the following code to check the information about the data frame, such as number of rows and columns, data types for each column, etc.')
    # code = '''df.info()''' 
    # st.code(code, language='python')

    #Allow users to check the results of the third code snippet by clicking the 'Check Results' button
    # import io 
    # buffer = io.StringIO()
    # df.info(buf=buffer)
    # s = buffer.getvalue()
    # if st.button('Check Results', key='3'):
    #     st.text(s)
    # else:
    #     st.write('---')

elif choose == "Conclusions":
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ## Conclusions:
    --------------
    As part of this Final project, together we learnt different aspects of building an end-to-end big data project - from development to deployment!            

    
    This project touched on various aspects of depvelopment such as - 
    - **Data Collection** — Even though the core dataset we used was provided by Spotify, we still needed to go and look for other data sources 
    to enhance the data and combine it with the core data set. This activity involved an API setup and parsing the dataset.
    - **Unsupervised Learning** — We decided to take an innovative approach where we are aiming for novelty where a given user is predicted into a 
    cluster and then computing a distance to recommend a set of tracks. Exploring different families of cluster algorithms and learning about 
    advantages and disadvantages to make the best selection as well as deciding which measure distance makes the most sense for our purposes.<br>
    - **Efficient Data Processing** — Midway through the project when we wanted to use the full 1M dataset we realized that it represents its own challenge and 
    we needed to rework the code to be able to not only run our analysis but to actually finalize the analysis. One thing that was a life saver was to develop 
    an SQLite database where the computing was reduced by 98%. Also by leveraging multiple API calls we were able to reduce the compute time from 40hours to 30minutes. 
    When dealing with this big of a dataset you need to get creative and write very efficient code.
    - **Big Data** — Dealing with such a large playlist data requires a lot of computing power. We relied on AWS services to train our model and deploy it as an endpoint.
    - **Deployment** — Nowadays, UX and overall Frontend is taken for granted but to actually put something up with models running in the background is not easy. 
    In this application we made a Streamlit app that can be deployed to a server and deployed to a web app.

    """
    st.markdown("<br>", unsafe_allow_html=True)

# def playlist_page():
#     st.subheader("User Playlist")
#     st.markdown('---')
#     playlist_uri = st.session_state.playlist_url.split('/')[-1].split('?')[0]
#     uri_link = 'https://open.spotify.com/embed/playlist/' + playlist_uri
#     components.iframe(uri_link, height=300)
#     return

# def get_recommendations(rec_type):
#     st.session_state.got_rec = False
#     st.session_state.got_feedback = False
#     st.session_state.app_mode = 'recommend'
#     st.session_state.rec_type = rec_type

# def insert_songs(placeholder, track_uris):
#     with placeholder.container():
#         for uri in track_uris:
#             uri_link = "https://open.spotify.com/embed/track/" + uri + "?utm_source=generator&theme=0"
#             components.iframe(uri_link, height=80)


# def log_output(new_text):
#     new_log = st.session_state.output
#     if new_text != 'None':
#         new_log = new_text + '\n' + st.session_state.output
#     if st.session_state.display_output:
#         st.session_state.output = st.session_state.log_holder.text_area('',value=new_log, height=500)

# def load_spr_ml_model():
#     st.session_state.ml_model = SPR_ML_Model()


# def model_page():
#     st.subheader("Select your preference")
#     Types_of_Features = ("Playlist", "Song")
#     st.session_state.user_selection = st.session_state.user_op
#     st.radio("Feature", Types_of_Features, key='user_selection', on_change=update_user_option)

#     if st.session_state.user_selection == "Playlist":
#         st.session_state.playlist_url = st.session_state.example_url
#         st.text_input("Playlist URI", key='playlist_url', on_change=update_playlist_url)
#         playlist_uri = st.session_state.playlist_url.split('/')[-1]
#         st.session_state.spr = SpotifyRecommendations(playlist_uri=playlist_uri)
#         st.session_state.spr.log_output = log_output
#         playlist_page()
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.button("Get Recommendations", key='pl', on_click=get_recommendations, args=('playlist',))
#         with st.expander("Here's how to find any Playlist URL in Spotify"):
#             st.write(""" 
#                 - Search for Playlist on the Spotify app
#                 - Right Click on the Playlist you like
#                 - Click "Share"
#                 - Choose "Copy link to playlist"
#             """)
#             st.markdown("<br>", unsafe_allow_html=True)
#             st.image(os.path.join(cwd, 'assets/images', 'spotify_get_playlist_uri.png'))


# def rec_page():
#     if 'spr' not in st.session_state:
#         st.error('Please select an option in User Input page')
#         return
    
#     if st.session_state.rec_type == 'playlist':
#         st.subheader('Recommendations based on Playlist:')
#     elif st.session_state.rec_type == 'last_month':
#         st.subheader('Recommendations based on your Last Month Favorites:')
#     elif st.session_state.rec_type == '6_months':
#         st.subheader('Recommendations based on your Six Months Favorites:')
#     else:
#         st.subheader('Recommendations based on your All Time Favorites:')
#     status_holder = st.empty()
#     rec_songsholder = st.empty()
#     user_fbholder = st.empty()

#     left_column, middle_column, right_column = st.columns(3)
#     with left_column:
#         fb_plotholder = st.empty()
#     with middle_column:
#         playlist_wordcloud_holder = st.empty()
#         user_cluster_all_holder = st.empty()
        
#     with right_column:
#         genre_wordcloud_holder = st.empty()
#         user_cluster_single_holder = st.empty()
#     if st.session_state.ml_model is None:
#         with status_holder:
#             with st.spinner('Loading ML Model...'):
#                 load_spr_ml_model()
#             st.success('ML Model Loaded!')
#     else:
#         log_output('ML Model already loaded')
    
#     if st.session_state.got_rec == False:
#         spr = st.session_state.spr
#         spr.set_ml_model(st.session_state.ml_model)
#         with status_holder:
#             with st.spinner('Getting Recommendations...'):
#                 spr.len_of_favs = st.session_state.rec_type
#                 spr.log_output = log_output
#                 st.session_state.rec_uris = spr.get_songs_recommendations(n=10)
#                 # st.session_state.genre_wordcloud_fig = spr.get_genre_wordcloud_fig()
#                 # st.session_state.playlist_wordcloud_fig = spr.get_playlist_wordcloud_fig()
#                 st.session_state.user_cluster_all_fig = spr.get_user_cluster_all_fig()
#                 st.session_state.user_cluster_single_fig = spr.get_user_cluster_single_fig()
#                 st.session_state.got_rec = True
#             st.success('Here are top 10 recommendations!')
#     else:
#         log_output('Showing already found recommendations')

#     insert_songs(rec_songsholder, st.session_state.rec_uris)

#     if st.session_state.got_feedback == False:
#         with user_fbholder:
#             c1, c2, c3, c4 = st.columns((1, 1, 1, 1))
#             with c1:
#                 st.button("Love it", key='love', on_click=add_feedback, args=('Love it',))
#             with c2:
#                 st.button("Like it", key='like', on_click=add_feedback, args=('Like it',))
#             with c3:
#                 st.button("Okay", key='okay', on_click=add_feedback, args=('Okay',))
#             with c4:
#                 st.button("Hate it", key='hate', on_click=add_feedback, args=('Hate it',))

#     with fb_plotholder:
#         try:
#             feedback_db = User_FeedbackDB()
#             fig = feedback_db.get_feedback_plot()
#             del feedback_db
#             if fig:
#                 st.subheader('User Feedback:')
#                 st.plotly_chart(fig, use_container_width=True)
#         except:
#             pass

#     # genre_wordcloud_holder.pyplot(st.session_state.genre_wordcloud_fig)
#     # playlist_wordcloud_holder.pyplot(st.session_state.playlist_wordcloud_fig)
#     user_cluster_all_holder.pyplot(st.session_state.user_cluster_all_fig)
#     user_cluster_single_holder.pyplot(st.session_state.user_cluster_single_fig)

    
        



# def main():
#     #spr_sidebar()
#     # if st.session_state.app_mode == 'dataset':
#     #     dataset_page()

#     if st.session_state.app_mode == 'model':
#         model_page()

#     if st.session_state.app_mode == 'recommend':
#         rec_page()

# if __name__ == '__main__':
#     main()
