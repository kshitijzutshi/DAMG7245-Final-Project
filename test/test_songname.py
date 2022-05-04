import os
from numpy.core.arrayprint import format_float_positional
import numpy as np
import pandas as pd
import pytest

cwd = os.getcwd()

# playlists_db_path = '../data/spotify_20K_playlists.db'

# conn = sqlite3.connect(playlists_db_path)

# Pytest fixtures decorator allows to connect the db once, be visible across the scope
# and then close connection when all tests complete
# @pytest.fixture(scope="session")
# def db_conn():
#     db = sqlite3
#     url = playlists_db_path
#     with db.connect(url) as conn:  # connection will be torn down after all tests finish
#         yield conn

# tracks_df = pd.read_sql('select * from tracks', conn)
tracks_df = pd.read_csv('test/tracks_10.csv')
track_name = ['Toxic', 'Rock Your Body', 'Run It!', 'Replay',
       'One Less Lonely Girl', 'Somebody To Love', 'Eye of the Tiger',
       'Stairway To Heaven', 'Sympathy For The Devil', 'Kashmir']


def test_answer():
    

    track_id1 = tracks_df[tracks_df['track_name'].str.lower() == track_name[0].lower()]['track_id']
    assert len(track_id1) > 0

    track_id2 = tracks_df[tracks_df['track_name'].str.lower() == track_name[1].lower()]['track_id']
    assert len(track_id2) > 0
    
    track_id3 = tracks_df[tracks_df['track_name'].str.lower() == track_name[2].lower()]['track_id']
    assert len(track_id3) > 0

    track_id4 = tracks_df[tracks_df['track_name'].str.lower() == track_name[3].lower()]['track_id']
    assert len(track_id4) > 0
    
    track_id5 = tracks_df[tracks_df['track_name'].str.lower() == track_name[4].lower()]['track_id']
    assert len(track_id5) > 0
    
    track_id6 = tracks_df[tracks_df['track_name'].str.lower() == track_name[5].lower()]['track_id']
    assert len(track_id6) > 0

    track_id7 = tracks_df[tracks_df['track_name'].str.lower() == track_name[6].lower()]['track_id']
    assert len(track_id7) > 0
    
    track_id8 = tracks_df[tracks_df['track_name'].str.lower() == track_name[7].lower()]['track_id']
    assert len(track_id8) > 0
    
    track_id9 = tracks_df[tracks_df['track_name'].str.lower() == track_name[8].lower()]['track_id']
    assert len(track_id9) > 0
    
    track_id10 = tracks_df[tracks_df['track_name'].str.lower() == track_name[9].lower()]['track_id']
    assert len(track_id10) > 0
    # track_id1 = tracks_df[tracks_df['track_name'].str.lower() == track_name[0].lower()]['track_id']
    # if len(track_id1) > 0:
    #     assert True

    # track_id2 = tracks_df[tracks_df['track_name'].str.lower() == track_name[1].lower()]['track_id']
    # if len(track_id2) > 0:
    #     assert True
    
    # track_id3 = tracks_df[tracks_df['track_name'].str.lower() == track_name[2].lower()]['track_id']
    # print(track_id3)
    # if len(track_id3) > 0:
    #     assert True

    # track_id4 = tracks_df[tracks_df['track_name'].str.lower() == track_name[3].lower()]['track_id']
    # if len(track_id4) > 0:
    #     assert True
    
    # track_id5 = tracks_df[tracks_df['track_name'].str.lower() == track_name[4].lower()]['track_id']
    # if len(track_id5) > 0:
    #     assert True
    
    # track_id6 = tracks_df[tracks_df['track_name'].str.lower() == track_name[5].lower()]['track_id']
    # if len(track_id6) > 0:
    #     assert True

    # track_id7 = tracks_df[tracks_df['track_name'].str.lower() == track_name[6].lower()]['track_id']
    # if len(track_id7) > 0:
    #     assert True
    
    # track_id8 = tracks_df[tracks_df['track_name'].str.lower() == track_name[7].lower()]['track_id']
    # if len(track_id8) > 0:
    #     assert True
    
    # track_id9 = tracks_df[tracks_df['track_name'].str.lower() == track_name[8].lower()]['track_id']
    # if len(track_id9) > 0:
    #     assert True
    
    # track_id10 = tracks_df[tracks_df['track_name'].str.lower() == track_name[9].lower()]['track_id']
    # if len(track_id10) > 0:
    #     assert True

    

    # for track in range(len(track_name)):
    #     track_id = tracks_df[tracks_df['track_name'].str.lower() == track_name[track].lower()]['track_id']
    #     # print(track_id)
    #     # assert len(track_id) > 0
    #     if len(track_id) > 0:
    #         assert True
        # else:
        #     assert False

test_answer()