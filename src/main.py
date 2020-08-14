
import my_songs_tool
from your_data import *
import pandas as pd
from time import sleep
from your_data import *

def run():
    """
    Run this function and all the will extract all the music from the JSON files and add
    the Spotify's features.
    """

    # Step 1: Get Authorization
    token = my_songs_tool.get_authorization(username, client_id, client_secret, redirect_uri, scope)

    # Step 2: Get streaming list of songs
    path = 'data/'
    streamings = my_songs_tool.get_streamings(path)
    print(f'You have {len(streamings)} streamings. Good job at listing Spotify')

    
if __name__ == '__main__':
    run()