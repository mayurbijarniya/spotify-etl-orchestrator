# Spotify ETL Data Engineering Project

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline for Spotify data from a playlist made by my running group using Python and AWS services.

## Project Overview

The ETL pipeline performs the following steps:

1. **Extract**: Fetches data from the Spotify API.
2. **Transform**: Processes and cleans the extracted data.
3. **Load**: Stores the transformed data into a target data warehouse or database.

## Repository Structure

- `spotify_data.ipynb`: Jupyter Notebook containing initial data extraction from the Spotify API and transformations to change the data from json to dataframes to make it easy to read.
- `spotify_etl_lambda.py`: Python script designed to be deployed as an AWS Lambda function for automating the ETL process.
- `sotify_etl_lambda_transform.py`: Python script for transforming the data within the AWS Lambda function.
- `spotify_snowflake_load.sql`: SQL script executed on snowflake to create integration, build a stage and utlizie snowpipes to load any new files that landed in s3

## Prerequisites

- Python 3.6 or higher
- AWS account with permissions to create Lambda functions
- Spotify Developer account with access to the Spotify API

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mayurbijarniya/sptoify_etl_de.git
   ```

2. **Set environment variables** (example names used by the code):
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`
   - AWS credentials are recommended to be provided via IAM roles for Lambda (avoid embedding keys in code)

![Image of Architecture](https://github.com/mayurbijarniya/sptoify_etl_de/blob/main/Copy%20of%20Spotify%20ETL%20Architecture%20Cloud.png)
