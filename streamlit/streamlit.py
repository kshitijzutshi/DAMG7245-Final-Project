from tkinter import font
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import base64
import numpy as np
import cv2
#from  PIL import ImageChops
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io 
import sqlite3 
import hashlib
import streamlit.components.v1 as components

from spotipy_client import *

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


logo = Image.open(r'./assets/images/logo.png')
profile = Image.open(r'./assets/images/twitter-logo.png')
spotify = Image.open(r'./assets/images/spotify.png')
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
if 'rec_uris' not in st.session_state:
    st.session_state.rec_uris = []

if 'user_op' not in st.session_state:
    st.session_state.user_op = 'Playlist'
def update_user_option():
    st.session_state.user_op = st.session_state.user_selection

if 'response_url' not in st.session_state:
    st.session_state.response_url = ''
def init_sp():
    st.session_state.spr.init_sp(st.session_state.response_url)

if 'example_url' not in st.session_state:
    st.session_state.example_url = 'Example: https://open.spotify.com/embed/playlist/37i9dQZF1DX0kbJZpiYdZl'
def update_playlist_url():
    st.session_state.example_url = st.session_state.playlist_url

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

#def spr_sidebar():
with st.sidebar:
    #model_button = st.button('Recommendation')
    st.image(spotify, width=300)
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
# if choose == "Recommendations":
#             st.session_state.app_mode = 'model'


logo = Image.open(r'./assets/images/logo.png')
profile = Image.open(r'./assets/images/twitter-logo.png')

# """### gif from local file"""
file_ = open(r'./assets/images/login.gif', "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


st.title('Spotify Music Recommendation App')
# Home is where user will login
if choose == "Home":
#     st.markdown(
#     f'<img src="data:image/gif;base64,{data_url}" alt="Login" width="750" height="300">',
#     unsafe_allow_html=True,
# )
#Add the cover image for the cover page. Used a little trick to center the image
    # left_column, right_column = st.columns(2)
    # # col1, col2 = st.columns([1,2])
    # with left_column: 
    #     left_column.subheader("Create New Account")
    #     new_user = st.text_input("Username")
    #     new_password = st.text_input("Password",type='password')

    #     if st.button("Signup"):
    #         #create_usertable()
    #         add_userdata(new_user,make_hashes(new_password), 10, datetime.datetime.now())
    #         st.success("You have successfully created a valid Account")
    #         st.info("Go to Login Menu to login")


    # col1 = st.columns([1])

    # with col1:
        # pics = {}
        # showWarningOnDirectExecution = False
    # user = {
    #         "fullname": fullname,
    #         "email": email,
    #         "password": password
    #     }
    # if submit_signup:
    #     # Create Search Query
    #     data = {'fullname':  [fullname],
    #             'email': [email],
    #             'api_count': [2]
    #     }

    #     df = pd.DataFrame(data, columns = ['fullname', 'email', 'api_count'])              # To display the header text using css style
    #     st.markdown(""" <style> .font {
    #     font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    #     </style> """, unsafe_allow_html=True)
    #     st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)
        
                  # To display brand log
        st.subheader("Login")
			# if password == '12345'
        username = st.text_input("User Name")
        password = st.text_input("User Password",type='password')
        #count = 0
        if st.button("Login"):
            # if password == '12345':
            #create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))
            
                
            if len(result):
                
                st.success("Logged In as {}".format(username))

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

        elif st.checkbox("Not a Exisiting User?"):
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password",type='password')

            if st.button("Signup"):
            #create_usertable()
                add_userdata(new_user,make_hashes(new_password), 10, datetime.datetime.now())
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")


    
        

elif choose == "Dataset":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Upload your photo here...</p>', unsafe_allow_html=True)
        
    with col2:               # To display brand logo
        st.image(logo,  width=150)
    #Add file uploader to allow users to upload photos
    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image,width=300)  

        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)

            converted_img = np.array(image.convert('RGB')) 
            gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
            inv_gray = 255 - gray_scale
            blur_image = cv2.GaussianBlur(inv_gray, (125,125), 0, 0)
            sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
            st.image(sketch, width=300)

elif choose == "Model":
#Add a file uploader to allow users to upload their project plan file
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your project plan</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Fill out the project plan template and upload your file here. After you upload the file, you can edit your project plan within the app.", type=['csv'], key="2")
    if uploaded_file is not None:
        Tasks=pd.read_csv(uploaded_file)
        Tasks['Start'] = Tasks['Start'].astype('datetime64')
        Tasks['Finish'] = Tasks['Finish'].astype('datetime64')
        
        grid_response = AgGrid(
            Tasks,
            editable=True, 
            height=300, 
            width='100%',
            )

        updated = grid_response['data']
        df = pd.DataFrame(updated) 
        
        if st.button('Generate Gantt Chart'): 
            fig = px.timeline(
                            df, 
                            x_start="Start", 
                            x_end="Finish", 
                            y="Task",
                            color='Completion Pct',
                            hover_name="Task Description"
                            )

            fig.update_yaxes(autorange="reversed")          #if not specified as 'reversed', the tasks will be listed from bottom up       
            
            fig.update_layout(
                            title='Project Plan Gantt Chart',
                            hoverlabel_bgcolor='#DAEEED',   #Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
                            bargap=0.2,
                            height=600,              
                            xaxis_title="", 
                            yaxis_title="",                   
                            title_x=0.5,                    #Make title centered                     
                            xaxis=dict(
                                    tickfont_size=15,
                                    tickangle = 0,
                                    rangeslider_visible=True,
                                    side ="top",            #Place the tick labels on the top of the chart
                                    showgrid = True,
                                    zeroline = True,
                                    showline = True,
                                    showticklabels = True,
                                    tickformat="%x\n",      #Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
                                    )
                        )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('---') 
   

elif choose == "Recommendations":
    st.session_state.app_mode = 'model'
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
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        #st.write('Please help us improve!')
        Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
        Email=st.text_input(label='Please Enter Your Email') #Collect user feedback
        Message=st.text_input(label='Please Enter Your Message') #Collect user feedback
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')

def playlist_page():
    st.subheader("User Playlist")
    st.markdown('---')
    playlist_uri = st.session_state.playlist_url.split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/playlist/' + playlist_uri
    components.iframe(uri_link, height=300)
    return

def get_recommendations(rec_type):
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
        st.button("Get Recommendations", key='pl', on_click=get_recommendations, args=('playlist',))
        with st.expander("Here's how to find any Playlist URL in Spotify"):
            st.write(""" 
                - Search for Playlist on the Spotify app
                - Right Click on the Playlist you like
                - Click "Share"
                - Choose "Copy link to playlist"
            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.image(os.path.join(cwd, 'images', 'spotify_get_playlist_uri.png'))


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

    
        



def main():
    #spr_sidebar()
    # if st.session_state.app_mode == 'dataset':
    #     dataset_page()

    if st.session_state.app_mode == 'model':
        model_page()

    if st.session_state.app_mode == 'recommend':
        rec_page()

if __name__ == '__main__':
    main()