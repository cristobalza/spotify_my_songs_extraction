import ast
import requests
from datetime import datetime
import spotipy
import spotipy.util as util
from os import listdir
from time import sleep
import pandas as pd

def get_authorization(user, 
              client_id,
              client_secret,
              redirect_uri,
              scope):
  
    token = util.prompt_for_user_token(username = user,scope=None,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    return token

def get_streamings(path='data/'):
    '''
    Returns a list of streamings from my data/ directory.
    Will not acquire track features.
    '''
    # Make sure the files you are scanning are the StreamingHistory JSON files
    files = [path + x for x in listdir('data') if x.split('.')[0][:-1] == 'StreamingHistory']
    
    all_streamings = []
    # Iterate through each of the StreamingHistory JSON files and iterate again to add the list
    for file in files: 
        with open(file, 'r', encoding='UTF-8') as f:
            # Read file
            new_streamings = ast.literal_eval(f.read())
            all_streamings += [streaming for streaming in new_streamings]
            
    # From the feature enTime, add the time and create datetime
    for streaming in all_streamings:
        streaming['datetime'] = datetime.strptime(streaming['endTime'], '%Y-%m-%d %H:%M')   
    return all_streamings


######################

def get_saved_ids(tracks, path = 'output/track_ids.csv'):
    track_ids = {track: None for track in tracks}
    folder, filename = path.split('/')
    if filename in listdir(folder):
        try:
            idd_dataframe = pd.read_csv('output/track_ids.csv', names = ['name', 'idd'])
            idd_dataframe = idd_dataframe[1:]                    #removing first row
            added_tracks = 0
            for index, row in idd_dataframe.iterrows():
                if not row[1] == 'nan':                          #if the id is not nan
                    track_ids[row[0]] = row[1]                    #add the id to the dict
                    added_tracks += 1
            print(f'Saved IDs successfully recovered for {added_tracks} tracks.')
        except:
            print('Error. Failed to recover saved IDs!')
            pass
    return track_ids

def get_saved_features(tracks, path = 'output/features.csv'):
    folder, file = path.split('/')
    track_features = {track:None for track in tracks}
    if file in listdir(folder):
        features_df = pd.read_csv(path, index_col = 0)
        n_recovered_tracks = 0
        for track in features_df.index:
            features = features_df.loc[track, :]
            if not features.isna().sum():          #if all the features are there
                track_features[track] = dict(features)
                n_recovered_tracks += 1
        print(f"Added features for {n_recovered_tracks} tracks.")
        return track_features
    else:
        print("Did not find features file.")
        return track_features

######################
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



    