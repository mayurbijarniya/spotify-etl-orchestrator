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
- `spotify_transformer.py`: AWS Lambda function that cleans and transforms raw JSON data into structured CSV format.
- `snowflake_setup.sql`: SQL script to configure Snowflake storage integrations, stages, and Snowpipes for automated data loading.

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
   - AWS credentials are recommended to be provided via IAM roles for Lambda (avoid embedding keys in code)

![Image of Architecture](https://github.com/mayurbijarniya/sptoify_etl_de/blob/main/Copy%20of%20Spotify%20ETL%20Architecture%20Cloud.png)
