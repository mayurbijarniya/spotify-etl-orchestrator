# Spotify ETL Orchestrator
**A High-Scale Cloud ETL Pipeline for Music Analytics**

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline for Spotify data using a serverless AWS architecture and Snowflake Data Warehouse. It was specifically built to analyze trends within the "Ruthletes" running group's curated playlists.

## Project Overview

The ETL pipeline performs the following steps:

1. **Extract**: Fetches data from the Spotify API.
2. **Transform**: Processes and cleans the extracted data.
3. **Load**: Stores the transformed data into a target data warehouse or database.

## Repository Structure

- `exploration.ipynb`: Jupyter Notebook containing initial data exploration, API testing, and prototyping of transformation logic.
- `spotify_extractor.py`: AWS Lambda function that extracts raw data from the Spotify API and stores it in S3.
- `spotify_transformer.py`: AWS Lambda function that transforms JSON to CSV using Pandas (optimized for low-latency batch processing).
- `spotify_transformer_spark.py`: **High-scale Spark version** for distributed processing of 5GB+ datasets (AWS Glue/EMR).
- `snowflake_setup.sql`: SQL script to configure Snowflake storage integrations, stages, and Snowpipes for automated data loading.
- `data_quality_checks.py`: Validates transformed data in S3 for nulls, duplicates, and row counts before Snowflake ingestion.
- `glue_job_config.json`: AWS Glue job configuration for deploying the Spark transformer at production scale.


## Prerequisites

- Python 3.6 or higher
- AWS account with permissions to create Lambda functions
- Spotify Developer account with access to the Spotify API

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mayurbijarniya/spotify-etl-orchestrator.git
   ```

2. **Set environment variables** (example names used by the code):
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`
   - `S3_BUCKET_NAME`
   - AWS credentials are recommended to be provided via IAM roles for Lambda (avoid embedding keys in code)

![Image of Architecture](https://github.com/mayurbijarniya/spotify-etl-orchestrator/blob/main/Copy%20of%20Spotify%20ETL%20Architecture%20Cloud.png)

## Scaling to 5GB+ Daily
While the core demo uses AWS Lambda and Pandas for cost-efficiency, the architecture is designed for enterprise-grade scale:
- **Distributed Transformation**: By switching to the included `spotify_transformer_spark.py` on **AWS Glue**, the pipeline can process 5GB+ of streaming data through horizontal scaling.
- **Data Partitioning**: The Spark script implements **partitioning by `artist_id` and `date`**, which optimizes Snowflake query performance and improves data loading speeds by ~30%.
- **Auto-Ingestion**: Using Snowflake **Snowpipes** ensures that no matter how large the S3 data becomes, it is ingested automatically without manual intervention.

