
import my_songs_tool
import connect_to_spotify
from your_data import *
import pandas as pd
from time import sleep


def run():
    """
    Run this function and all the will extract all the music from the JSON files and add
    the Spotify's features.
    """
    # Step 1: Get Authorization
     #recover streamings history
    token = my_songs_tool.get_authorization(username, client_id, 
                              client_secret, redirect_uri, scope)
    
    streamings = my_songs_tool.get_streamings()
    print(f'Recovered {len(streamings)} streamings.')

    
    #getting a list of unique tracks in our history
    tracks = set([streaming['trackName'] for streaming in streamings])
    print(f'Discovered {len(tracks)} unique tracks.')
    
    #getting saved ids for tracks
    track_ids = my_songs_tool.get_saved_ids(tracks)
    
    # Step  : Collect IDs
    # my_songs_tool.collect_1(track_ids, token)

    #recovering saved features
    track_features = my_songs_tool.get_saved_features(tracks)
    tracks_without_features = [track for track in tracks if track_features.get(track) is None]
    tracks_with_features = [track for track in tracks if track_features.get(track) is not None]
    print(f"There are still {len(tracks_without_features)} tracks without features.")
    print(f"There are {len(tracks_with_features)} tracks WITH features")

    # Step :features collection
    # features_df = connect_to_spotify.collect_2(track_ids, token, track_features, tracks )
    # print(features_df.head())

    
if __name__ == '__main__':
    run()