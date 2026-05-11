import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, to_date, from_unixtime
from datetime import datetime

"""
Spotify ETL: Spark Transformation Script (Glue/EMR Version)
Designed to handle 5GB+ daily datasets through distributed processing.
"""

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("SpotifyETLTransform") \
        .getOrCreate()

    # S3 Buckets from environment variables
    bucket_name = os.environ.get('S3_BUCKET_NAME', 'spotify-etl-orchestrator-bucket')
    raw_path = f"s3://{bucket_name}/raw_data/to_processed/*.json"
    transformed_path = f"s3://{bucket_name}/transformed_data/"

    # 1. Read raw JSON data
    # Note: Spark's distributed reader is essential for 5GB+ datasets
    df_raw = spark.read.option("multiline", "true").json(raw_path)

    # 2. Explode the track items
    df_tracks = df_raw.selectExpr("explode(items) as item")

    # --- SONG TRANSFORMATION ---
    songs_df = df_tracks.select(
        col("item.track.id").alias("song_id"),
        col("item.track.name").alias("song_name"),
        col("item.track.duration_ms").alias("duration_ms"),
        col("item.track.external_urls.spotify").alias("url"),
        col("item.track.popularity").alias("popularity"),
        col("item.added_at").alias("song_added"),
        col("item.track.album.id").alias("album_id"),
        col("item.track.album.artists")[0]["id"].alias("artist_id")
    ).dropDuplicates(["song_id"])

    # --- ALBUM TRANSFORMATION ---
    albums_df = df_tracks.select(
        col("item.track.album.id").alias("album_id"),
        col("item.track.album.name").alias("name"),
        col("item.track.album.release_date").alias("release_date"),
        col("item.track.album.total_tracks").alias("total_tracks"),
        col("item.track.album.external_urls.spotify").alias("url")
    ).dropDuplicates(["album_id"])

    # --- ARTIST TRANSFORMATION ---
    artists_df = df_tracks.select(
        col("item.track.album.artists")[0]["id"].alias("artist_id"),
        col("item.track.album.artists")[0]["name"].alias("artist_name"),
        col("item.track.album.artists")[0]["href"].alias("external_url")
    ).dropDuplicates(["artist_id"])

    # 3. Write transformed data back to S3 in Parquet format
    # Using Parquet + Partitioning is key to the 30% optimization claim
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    songs_df.write.mode("append") \
        .partitionBy("artist_id") \
        .parquet(f"{transformed_path}songs_data/dt={current_date}/")

    albums_df.write.mode("append") \
        .parquet(f"{transformed_path}albums_data/dt={current_date}/")

    artists_df.write.mode("append") \
        .parquet(f"{transformed_path}artists_data/dt={current_date}/")

    print(f"Successfully transformed and loaded data for {current_date}")

if __name__ == "__main__":
    main()
