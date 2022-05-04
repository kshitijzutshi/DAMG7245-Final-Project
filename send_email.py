import smtplib, ssl
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv
load_dotenv()

cwd = os.getcwd()

user_data_path = os.path.join(cwd, 'streamlit', 'new.csv')

user_data_df = pd.read_csv(user_data_path)


sender_email = os.getenv('EMAIL_ADDRESS')

sender_password = os.getenv('EMAIL_PASSWORD')

receiver_email = os.getenv('EMAIL_ADDRESS')


# For each user in the csv file send the MIMEMULTIPART message
users_list = user_data_df['Username']

user_email_ids = user_data_df['email_id']

for user in range(0, len(users_list)):

    rec_uri_id_list = user_data_df['rec_song_uri'][user].split(',')
    # print(rec_uri_id_list)
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email_ids[user]
    msg['Subject'] = Header('Your Spotify Weekly Recommendations are here', 'utf-8').encode()
    

    # html = """\
    # <html>
    #   <body>
    #     <p>Hi</p>
    #      <iframe src="https://open.spotify.com/embed/track/4LRPiXqCikLlN15c3yImP7?utm_source=generator&theme=0" height="80"></iframe>
    #      <iframe src="https://open.spotify.com/embed/track/1rDQ4oMwGJI7B4tovsBOxc?utm_source=generator&theme=0" height="80"></iframe> 
    #   </body>
    # """
    html = f'<h3>Hi {users_list[user]}, Following are the recommended songs based on your last song search - </h3><br><ol><li>https://open.spotify.com/embed/track/{rec_uri_id_list[0]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[1]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[2]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[3]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[4]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[5]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[6]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[7]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[8]}?utm_source=generator&theme=0</li><li>https://open.spotify.com/embed/track/{rec_uri_id_list[9]}?utm_source=generator&theme=0</li></ol>'
    msg_content = MIMEText(html, 'html')
    msg.attach(msg_content)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email_ids[user], msg.as_string())

# ref - https://www.youtube.com/watch?v=JRCJ6RtE3xU&ab_channel=CoreySchafer
