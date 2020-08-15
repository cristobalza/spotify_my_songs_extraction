import ast
import requests
from datetime import datetime
from os import listdir
import pandas as pd



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

def get_saved_ids(songs, path = 'output/track_ids.csv'):
    """
    Returns a dictionary. If the file has been created before you 
    """
    # Create empty dictionary 
    song_ids = {track: None for track in songs}
    # Split the output directory and the respective file
    directory, file_name = path.split('/')
    # Iterate through the files in the output directory
    if file_name in listdir(directory):
        try:
            # Create dataframe of songs and ids
            song_ids_df = pd.read_csv('output/track_ids.csv', names = ['name', 'idd'])
            # Removes the first row of df
            song_ids_df = song_ids_df[1:]   
            # Create count variable                 
            count_songs = 0
            # Iterate through each songs
            for _ , row in song_ids_df.iterrows():
                if row[1] != 'nan':                         
                    song_ids[row[0]] = row[1]                  
                    count_songs += 1
            print(f'Saved IDs successfully recovered for {count_songs} tracks.')
        except:
            print('Error. Failed to recover saved IDs!')
            pass
    return song_ids

def get_saved_features(songs, path = 'output/features.csv'):
    directory, file_name = path.split('/')
    song_features = {s:None for s in songs}
    if file_name in listdir(directory):
        features_df = pd.read_csv(path, index_col = 0)
        count_songs = 0
        for song in features_df.index:
            features = features_df.loc[song, :]
            if not features.isna().sum():         
                song_features[song] = dict(features)
                count_songs += 1
        print(f"Added features for {count_songs} tracks.")
        return song_features
    else:
        print("Did not find features file.")
        return song_features

def collect_3(streamings, track_features):
    streamings_with_features = []
    for streaming in streamings:
        track = streaming['trackName']
        features = track_features[track]
        if features:
            streamings_with_features.append({'name': track, **streaming, **features})
    print(f'Added features to {len(streamings_with_features)} streamings.')
    print('Saving streamings...')
    df_final = pd.DataFrame(streamings_with_features)
    df_final.to_csv('output/final.csv')
    perc_featured = round(len(streamings_with_features) / len(streamings) *100, 2)
    print(f"Done! Percentage of streamings with features: {perc_featured}%.") 


    