import ast
import requests
from datetime import datetime
import spotipy
import spotipy.util as util
from os import listdir
from time import sleep
import pandas as pd
import my_songs_tool

def get_authorization(user, 
              client_id,
              client_secret,
              redirect_uri,
              scope):
  
    token = util.prompt_for_user_token(username = user,scope=None,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    return token

def get_api_features(track_id, token):
    sp = spotipy.Spotify(auth=token)
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return None

def get_api_id(track_name, token, artist= None):
    
    '''Performs a query on Spotify API to get a track ID.
    '''
   
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ' + token,
    }
    
    params = [
    ('q', track_name),
    ('type', 'track'),
    ]
    
    if artist: 
        params.append(('artist', artist))
        
    try:
        response = requests.get('https://api.spotify.com/v1/search', headers = headers, params = params, timeout = 5)
        json = response.json()
        first_result = json['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except:
        return None


def map_song_id(track_ids, token):

    #using spotify API to recover track ids
    #note: this methods works only for tracks. 
    #podcasts and other items will be ignored.
    print('Connecting to Spotify to recover tracks IDs.')
    # sleep(3)
    for track, idd in track_ids.items(): 
        if idd is None: 
            try:
                found_idd = get_api_id(track, token)
                track_ids[track] = found_idd
                print(track, found_idd)
            except:
                pass
    
    #how many tracks did we identify? 
    identified_tracks = [track for track in track_ids if track_ids[track] is not None]
    print(f'Successfully recovered the ID of {len(identified_tracks)} tracks.')
    
    #how many items did we fail to identify? 
    n_tracks_without_id = len(track_ids) - len(identified_tracks)
    print(f"Failed to identify {n_tracks_without_id} items. "
            "However, some of these may not be tracks (e.g. podcasts).")
    
    #using pandas to save tracks ids (so we don't have to API them in the future)
    ids_path = 'output/track_ids.csv'
    ids_dataframe = pd.DataFrame.from_dict(track_ids, orient = 'index')
    ids_dataframe.to_csv(ids_path)
    print(f'track ids saved to {ids_path}.')

def collect_2(track_ids, token, track_features, tracks):
    print('Connecting to Spotify to extract features...')
    acquired = 0
    for track, idd in track_ids.items(): 
        # if idd is not None and track in tracks_without_features:
        try:
            features = get_api_features(idd, token)
            track_features[track] = features
            if features:
                acquired += 1
                print(f'Acquired features: {track}. Song #: {acquired}')
        except:
            features = None
    tracks_without_features = [track for track in tracks if track_features.get(track) is None]
    print(f'Successfully recovered features of {acquired} tracks.')
    if len(tracks_without_features):
        print(f'Failed to identify {len(tracks_without_features)} items. Some of these may not be tracks.')
    
    #saving features 
    features_df = pd.DataFrame(track_features).T
    features_df.to_csv('output/features.csv')
    return features_df
