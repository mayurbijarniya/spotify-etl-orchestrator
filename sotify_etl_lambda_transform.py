import json
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO 

# Convert mixed values to a consistent datetime format
def handle_date(value):
    try:
        # Use the function as is if it can be converted to a date
        return pd.to_datetime(value)
    except ValueError:
        # If that fails, we give it a default value of first of that year!
        return pd.to_datetime(value + '-01-01')



def album(data):
    ruthletes_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        album_element = {'album_id':album_id,'name':album_name,
                        'release_date':album_release_date,
                            'total_tracks':album_total_tracks,'url':album_url} ## dictinory with all the keys I am interested in
        ruthletes_list.append(album_element)
    return ruthletes_list

def artist(data):
    ruthletes_artists_list = []
    for row in data['items']:
        for key, value in row.items():
            if key == "track":
                for artist in value['artists']:
                    artist_dict = {'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                    ruthletes_artists_list.append(artist_dict) 
    return ruthletes_artists_list

def songs(data):
    ruthletes_song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                        'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                        'artist_id':artist_id
                    }
        ruthletes_song_list.append(song_element)
    return ruthletes_song_list

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    bucket = 'spotify-ruthletes-project-etl'
    key = 'raw_data/to_processed/'
    spotify_data = []
    spotify_keys = []

    for file in s3.list_objects_v2(Bucket=bucket, Prefix=key)['Contents']:
        file_key = file['Key']
        if file_key.endswith('.json'):
            response = s3.get_object(Bucket=bucket, Key=file_key)
            content = response['Body']
            jsonObject = json.loads(content.read())
            spotify_data.append(jsonObject)
            spotify_keys.append(file_key)
    
    for data in spotify_data:
        ruthletes_album = album(data)
        ruthletes_artist = artist(data)
        ruthletes_song = songs(data)
    
        ruthletes_album_df = pd.DataFrame(ruthletes_album)
        ruthletes_album_df = ruthletes_album_df.drop_duplicates(subset='album_id')

        ruthletes_artist_df = pd.DataFrame(ruthletes_artist)
        ruthletes_artist_df = ruthletes_artist_df.drop_duplicates(subset='artist_id')

        ruthletes_song_df = pd.DataFrame(ruthletes_song)
        ruthletes_song_df = ruthletes_song_df.drop_duplicates(subset='song_id')

        ruthletes_album_df['release_date'] = ruthletes_album_df['release_date'].apply(handle_date)
        ruthletes_song_df['song_added'] = ruthletes_song_df['song_added'].apply(handle_date)

        song_key = 'transformed_data/songs_data/song_transformed_'+str(datetime.now())+ '.csv'
        song_buffer = StringIO()
        ruthletes_song_df.to_csv(song_buffer)
        song_content = song_buffer.getvalue()
        s3.put_object(Bucket=bucket,Key=song_key, Body=song_content) 

        album_key = 'transformed_data/albums_data/album_transformed_'+str(datetime.now())+ '.csv'
        album_buffer = StringIO()
        ruthletes_album_df.to_csv(album_buffer)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket=bucket,Key=album_key, Body=album_content)

        artist_key = 'transformed_data/artists_data/artist_transformed_'+str(datetime.now())+ '.csv'
        artist_buffer = StringIO()
        ruthletes_artist_df.to_csv(artist_buffer)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket=bucket,Key=artist_key, Body=artist_content)