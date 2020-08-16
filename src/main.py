import my_songs_tool
import connect_to_my_spotify
from your_data import *

def run():
    """
    Run this function and all the will extract all the music from the JSON files and add
    the Spotify's features by connecting to the platform's API.
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
    
    # Step 3: Map the songs to their respective id in a dictioary.
    # Creates an empty dictionary of each song of the streaming history with a None value.
    songs_ids = {track: None for track in songs}
    songs_ids = connect_to_my_spotify.map_song_id(songs_ids, token)

    # Step 4: Map the songs with their respective features by usig their ids####
    # Note for the reader: Using the id is the most effective way to extract the Spotify's features of each song.
    song_features = {track: None for track in songs}
    song_features = connect_to_my_spotify.map_song_feature(songs_ids, token, song_features, songs )

    # Step 5: Join the streaming and features together
    print('Adding features to streamings...')
    my_songs_tool.join_streamings_with_song_features(streamings, song_features)

    
if __name__ == '__main__':
    run()