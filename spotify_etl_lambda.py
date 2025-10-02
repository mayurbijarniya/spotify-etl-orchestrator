import json
import os ##To get environment variables
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3  ##dump the json into s3 and this helps with that
from datetime import datetime

def lambda_handler(event, context):
    
    # Read Spotify credentials from environment variables
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists('spotify')
    
    ruthletes_link = "https://open.spotify.com/playlist/4mPc6hwGfLZ67ohGEK4YMZ"
    playlist_URI = ruthletes_link.split("/")[-1]
    
    spotify_data = sp.playlist_tracks(playlist_URI)   

    print(spotify_data)
    
    client = boto3.client('s3')
    
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    cilent.put_object(
        Bucket="spotify-ruthletes-project-etl",
        Key="raw_data/to_processed/" + filename,
        Body=json.dumps(spotify_data)
        )
    