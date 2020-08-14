
import streaming_music
from your_data import *
import pandas as pd
from time import sleep
from your_data import *

def run():

    # Obtain access through the API
    token = streaming_music.get_token(username, client_id, client_secret, redirect_uri, scope)
    print(token)
    
if __name__ == '__main__':
    run()