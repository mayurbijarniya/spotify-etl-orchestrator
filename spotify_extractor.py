import json
import os ##To get environment variables
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3  ##dump the json into s3 and this helps with that
from datetime import datetime

def lambda_handler(event, context):
    
    # Read credentials and bucket from environment variables
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    bucket_name = os.environ.get('S3_BUCKET_NAME')

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Target playlist for the Ruthletes running group
    ruthletes_link = "https://open.spotify.com/playlist/4mPc6hwGfLZ67ohGEK4YMZ"
    playlist_URI = ruthletes_link.split("/")[-1]
    
    spotify_data = sp.playlist_tracks(playlist_URI)   
    
    client = boto3.client('s3')
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    # Upload raw JSON data to S3
    client.put_object(
        Bucket=bucket_name,
        Key="raw_data/to_processed/" + filename,
        Body=json.dumps(spotify_data)
        )
    