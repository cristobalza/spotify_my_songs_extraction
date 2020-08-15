import my_songs_tool
import connect_to_my_spotify
from your_data import *
import pandas as pd
from time import sleep


def summary(summary_steamings):
    return summary_steamings



def run():
    """
    Run this function and all the will extract all the music from the JSON files and add
    the Spotify's features.
    """
    # Step 1: Get Authorization
    token = connect_to_my_spotify.get_authorization(username, client_id, client_secret, redirect_uri, scope)
    
    # Step 2: Parse the JSON files to obtain the data from each StreamingHistory.json file
    streamings = my_songs_tool.get_streamings()
    print(f"Number of streamings recovered from extraction: {len(streamings)} streamings.")

    # Step 2: From the streaming history, obtain the number of unique songs. ONLY songs.
    # Why? - Use the unique list to map their respective IDs.
    songs = set([streaming['trackName'] for streaming in streamings])
    print(f'Extracted {len(songs)} unique songs.')
    
    
    # songs_ids = my_songs_tool.get_saved_ids(songs)
    
    # Step 3: Map the songs to their respective id in a dictioary.
    songs_ids = {track: None for track in songs}
    connect_to_my_spotify.map_song_id(songs_ids, token)
    print(songs_ids)

    #recovering saved features
    # song_features = my_songs_tool.get_saved_features(songs)
    # songs_without_features = [track for track in songs if song_features.get(track) is None]
    # songs_with_features = [track for track in songs if song_features.get(track) is not None]
    # print(f"There are still {len(songs_without_features)} songs without features.")
    # print(f"There are {len(songs_with_features)} songs WITH features")

    # Step :features collection ####
    song_features = {track: None for track in songs}
    features_df = connect_to_my_spotify.collect_2(songs_ids, token, song_features, songs )
    print(features_df.head())
    print(f"The shape of the dataframe {features_df.shape}")

    # #joining features and streamings
    print('Adding features to streamings...')
    my_songs_tool.collect_3(streamings, song_features)

    
if __name__ == '__main__':
    run()