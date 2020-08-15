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




def join_streamings_with_song_features(streamings, track_features):
    streamings_with_features = []
    for streaming in streamings:
        track = streaming['trackName']
        features = track_features[track]
        if features:
            streamings_with_features.append({'name': track, **streaming, **features})
    print(f'Added features to {len(streamings_with_features)} streamings.')
    print('Saving streamings...')
    df_final = pd.DataFrame(streamings_with_features)
    df_final.to_csv('output/cristobal_streaming_history_with_features.csv')
    perc_featured = round(len(streamings_with_features) / len(streamings) *100, 2)
    print(f"Done! Percentage of streamings with features: {perc_featured}%.") 


    