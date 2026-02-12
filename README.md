# IPEDS End-to-End Data Engineering Project

## Overview
The purpose of this project is to develop an end-to-end data pipeline that analyzes the cost of tuition for colleges reporting Integrated Postsecondary Education Data System (IPEDS) data for compliance and public transparency.

This project is designed to simulate a real-world data engineering and analytics workflow, from ingestion to cloud deployment.

## Project Goals
This project aims to achieve the following:

1. Ingest IPEDS data from the Education Data Portal API into a SQLite database.
2. Transform raw data into analytics-ready tables using SQL and Python.
3. Develop an interactive dashboard using Python.
4. Publish the dashboard as a web-accessible HTML application.
5. Deploy the dashboard to the cloud using AWS.
6. Automate data refreshes based on API update schedules.

## Data Source
Data is sourced from the Urban Institute Education Data Portal API:
https://educationdata.urban.org/

This API provides publicly available IPEDS data for U.S. higher education institutions.

## Data Ingestion
During the ingestion phase, the API provided by the Education Data Portal is used to extract institutional and tuition data.  
The extracted data is stored in a local SQLite database as the raw data layer of the pipeline.

## AI Usage Disclosure
Some portions of this project utilize AI-assisted code generation to improve development efficiency.  
All AI-generated code is reviewed, tested, and clearly commented where applicable.
