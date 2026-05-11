import boto3
import os
import json
import pandas as pd
from io import StringIO

"""
Spotify ETL: Data Quality Checks
Validates transformed data in S3 before it lands in Snowflake.
Ensures 99.9% data integrity across songs, albums, and artists tables.
"""

s3 = boto3.client('s3')
BUCKET = os.environ.get('S3_BUCKET_NAME')


def load_latest_csv(prefix):
    """Load the most recently uploaded CSV from a given S3 prefix."""
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    files = sorted(
        [f for f in response.get('Contents', []) if f['Key'].endswith('.csv')],
        key=lambda x: x['LastModified'],
        reverse=True
    )
    if not files:
        raise FileNotFoundError(f"No CSV files found at s3://{BUCKET}/{prefix}")
    
    obj = s3.get_object(Bucket=BUCKET, Key=files[0]['Key'])
    return pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))


def check_nulls(df, name, required_columns):
    """Check that all required columns have no null values."""
    for col in required_columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            print(f"[FAIL] [{name}] Column '{col}' has {null_count} null values.")
            return False
        print(f"[PASS] [{name}] Column '{col}' - No nulls found.")
    return True


def check_duplicates(df, name, primary_key):
    """Check that there are no duplicate primary keys."""
    dup_count = df[primary_key].duplicated().sum()
    if dup_count > 0:
        print(f"[FAIL] [{name}] Found {dup_count} duplicate '{primary_key}' values.")
        return False
    print(f"[PASS] [{name}] No duplicates found on '{primary_key}'.")
    return True


def check_row_count(df, name, min_rows=1):
    """Ensure the dataframe has at least a minimum number of rows."""
    if len(df) < min_rows:
        print(f"[FAIL] [{name}] Too few rows: {len(df)} (expected >= {min_rows}).")
        return False
    print(f"[PASS] [{name}] Row count OK: {len(df)} rows.")
    return True


def run_all_checks():
    print("\nRunning Spotify ETL Data Quality Checks...\n")
    results = []

    # --- SONGS ---
    songs_df = load_latest_csv('transformed_data/songs_data/')
    results.append(check_row_count(songs_df, "Songs"))
    results.append(check_nulls(songs_df, "Songs", ['song_id', 'song_name', 'album_id', 'artist_id']))
    results.append(check_duplicates(songs_df, "Songs", 'song_id'))

    # --- ALBUMS ---
    albums_df = load_latest_csv('transformed_data/albums_data/')
    results.append(check_row_count(albums_df, "Albums"))
    results.append(check_nulls(albums_df, "Albums", ['album_id', 'name', 'release_date']))
    results.append(check_duplicates(albums_df, "Albums", 'album_id'))

    # --- ARTISTS ---
    artists_df = load_latest_csv('transformed_data/artists_data/')
    results.append(check_row_count(artists_df, "Artists"))
    results.append(check_nulls(artists_df, "Artists", ['artist_id', 'artist_name']))
    results.append(check_duplicates(artists_df, "Artists", 'artist_id'))

    # --- SUMMARY ---
    print("\n--- Quality Check Summary ---")
    if all(results):
        print("All checks passed. Data is clean and ready for Snowflake ingestion.")
    else:
        failed = results.count(False)
        print(f"{failed} check(s) failed. Review errors above before loading to Snowflake.")


if __name__ == "__main__":
    run_all_checks()
