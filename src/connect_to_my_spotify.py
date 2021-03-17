import requests
import spotipy
import spotipy.util as util
from time import sleep
import pandas as pd
import my_songs_tool

def get_authorization(user, client_id, client_secret, redirect_uri, scope):
    """
    Get Authorizationg from Spotify API.

    All parameters come from your_data.py, where you are supposed to input your personal Spotify information.
    """
    token = util.prompt_for_user_token(username = user,scope=None,
                                        client_id=client_id,
                                        client_secret=client_secret,
                                        redirect_uri=redirect_uri
                                        )
    return token

def get_api_features(song_id, token):
    """
    Creates a Spotify API client using the token.
    Returns audio features for one song using the ID as access key.

    Parameters
    ----------

    song_id : the ID of a particular song
    token   : authorization to access the Spotify's API
    """
    sp = spotipy.Spotify(auth=token)
    try:
        features = sp.audio_features([song_id])
        return features[0]
    except:
        return None

def get_api_id(song_name, token):
    """
    Returns the ID of a song
    
    Parameters
    ----------
    
    song_name : Name of the song of interest
    token     : authorization to access the Spotify's API
    """ 
    params = [('q', song_name),('type', 'track'),]
    try:
        response = requests.get('https://api.spotify.com/v1/search', headers= {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer ' + token,}, 
            params = params,
            timeout = 5)
        json = response.json()
        first_result = json['tracks']['items'][0]
        song_id = first_result['id']
        return song_id
    except:
        return None


def map_song_id(songs_ids, token):
    """
    Returns a mapping of each song of the streaming list to their respective Spotify ID.
    
    Parameters
    ----------
    
    songs_ids : dictionary of each song with a None value. This function fills the empty values.
    token     : authorization to access the Spotify's API
    """
    print('Connecting to Spotify to recover tracks IDs.')
    for curr_song, id_api in songs_ids.items(): 
        if id_api is None: 
            try:
                curr_id = get_api_id(curr_song, token)
                songs_ids[curr_song] = curr_id
                print(f"|| Name of song : {curr_song} || ID : {curr_id} ||")
            except:
                pass
    # API Summary
    items_with_api = [curr_song for curr_song in songs_ids if songs_ids[curr_song] is not None]
    print(f'Successfully extracted the ID of {len(items_with_api)} songs.')
    
    items_with_no_api = len(songs_ids) - len(items_with_api)
    print(f"Failed to extract {items_with_no_api} items. "
            "However, some of these may not be songs (e.g. podcasts, videos).")
    return songs_ids

def map_song_feature(songs_ids, token, song_features, songs_list):
    """
    Using the ID of a song, add the respective features from the Spotify's API.
    Then function proceeds to save the file in the ./output/ directory
    Returns the mapping of each song and their respective features. 

    Note for the reader: This is NOT the streaming history processing.

    Parameters
    ----------

    songs_ids     : Dictionary of Song Names and their IDs
    token         : Key authorization
    song_features : Dictionary of song and their features
    songs_list    : List of songs
    """
    print('Connecting to Spotify to extract features...')
    number = 0
    for song, idd in songs_ids.items(): 
        try:
            features = get_api_features(idd, token)
            song_features[song] = features
            if features:
                number += 1
                print(f'Added features to: {song}. Song #: {number}')
        except:
            features = None
    # Summary
    items_without_features = [song for song in songs_list if song_features.get(song) is None]
    print(f'Successfully recovered features of {number} songs.')
    if len(items_without_features):
        print(f'Failed to identify {len(items_without_features)} items. Some of these may not be songs.')
    
    # Save song features
    features_df = pd.DataFrame(song_features).T
    features_df.to_csv('output/cristobal_songs_features.csv')
    return song_features
