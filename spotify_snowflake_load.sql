create database spotify_db;

create or replace table spotify_db.public.song(

`song_id` string, 
  `song_name` string, 
  `duration_ms` bigint, 
  `url` string, 
  `popularity` bigint, 
  `song_added` string, 
  `album_id` string, 
  `artist_id` string
);
CREATE  TABLE spotify_db.public.albums(
  `album_id` string, 
  `name` string, 
  `release_date` string, 
  `total_tracks` bigint, 
  `url` string);

CREATE TABLE spotify_db.public.artists(
  `artist_id` string, 
  `artist_name` string, 
  `external_url` string);


CREATE OR REPLACE STORAGE INTEGRATION s3_spotify_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  -- Replace the placeholder below with your AWS role ARN at deployment time
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ROLE_NAME>'
  ENABLED = TRUE
  -- Replace the placeholder below with your S3 bucket/paths
  STORAGE_ALLOWED_LOCATIONS = ('s3://<S3_BUCKET_NAME>/')
  COMMENT = 'Create connection to s3';
DESC INTEGRATION s3_spotify_int;

CREATE OR REPLACE schema spotify_db.file_format;

CREATE OR REPLACE FILE FORMAT spotify_db.file_format.csv_file_format
TYPE = 'CSV'
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
null_if = ('NULL','null')
empty_field_as_null = True;


//Creating the stages for each table
CREATE or replace STAGE my_stage_integration   --access environment from external source (AUTHENTICATE AWS but this should not be done as keys are exposed)
URL = 's3://spotify-ruthletes-project-etl/transformed_data/albums_data/'
Storage_integration = s3_spotify_int
file_format = spotify_db.file_format.csv_file_format;

list @SPOTIFY_DB.FILE_FORMAT.MY_STAGE_INTEGRATION;

COPY INTO spotify_db.public.albums
FROM @my_stage_integration
FILE_FORMAT = (FORMAT_NAME = 'spotify_db.file_format.csv_file_format');

select * from spotify_db.public.albums;

CREATE or replace STAGE my_stage_integration_songs   --access environment from external source (AUTHENTICATE AWS but this should not be done as keys are exposed)
URL = 's3://spotify-ruthletes-project-etl/transformed_data/songs_data/'
Storage_integration = s3_spotify_int
file_format = spotify_db.file_format.csv_file_format;

CREATE or replace STAGE my_stage_integration_artists   --access environment from external source (AUTHENTICATE AWS but this should not be done as keys are exposed)
URL = 's3://spotify-ruthletes-project-etl/transformed_data/artists_data/'
Storage_integration = s3_spotify_int
file_format = spotify_db.file_format.csv_file_format;

COPY INTO spotify_db.public.song
FROM @my_stage_integration_songs
FILE_FORMAT = (FORMAT_NAME = 'spotify_db.file_format.csv_file_format');

COPY INTO spotify_db.public.artists
FROM @my_stage_integration_artists
FILE_FORMAT = (FORMAT_NAME = 'spotify_db.file_format.csv_file_format');

CREATE OR REPLACE SCHEMA SPOTIFY_DB.PIPES;

//Create the pipes for each table
CREATE OR REPLACE PIPE SPOTIFY_DB.PIPES.SPOTIFY_ALBUMS_PIPE
  AUTO_INGEST = TRUE
  AS
  COPY INTO SPOTIFY_DB.PUBLIC.ALBUMS
  FROM @SPOTIFY_DB.FILE_FORMAT.MY_STAGE_INTEGRATION;
CREATE OR REPLACE PIPE SPOTIFY_DB.PIPES.SPOTIFY_SONGS_PIPE
  AUTO_INGEST = TRUE
  AS
  COPY INTO SPOTIFY_DB.PUBLIC.SONG
  FROM @SPOTIFY_DB.FILE_FORMAT.MY_STAGE_INTEGRATION_SONGS;
CREATE OR REPLACE PIPE SPOTIFY_DB.PIPES.SPOTIFY_ARTISTS_PIPE
  AUTO_INGEST = TRUE
  AS
  COPY INTO SPOTIFY_DB.PUBLIC.ARTISTS
  FROM @SPOTIFY_DB.FILE_FORMAT.MY_STAGE_INTEGRATION_ARTISTS;

DESC PIPE SPOTIFY_DB.PIPES.SPOTIFY_ARTISTS_PIPE;

//Verifying
select count(*) from spotify_db.public.albums; //76 --> 86
select count(*) from spotify_db.public.artists; //316 --> 326
select count(*) from spotify_db.public.song; //308 -->318
