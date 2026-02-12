import requests
import sqlite3
import pandas as pd
import logging
from logger import get_logger
from datetime import datetime

PATH_DB = "ipeds.db"

#This will log the progress of the script. Only use when necessary.
log = get_logger()

#This will contain all out api calls. We can add or remove as needed.
url_dict = {
    "tuition":"https://educationdata.urban.org/api/v1/college-university/ipeds/academic-year-tuition/2021/",
    "directory":"https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2021/",
}

def api_call(api_name : str, url : str) -> pd.DataFrame:
    log.info(f"{api_name} API call started.")
    next_url = url
    storage = []
    response = requests.get(url,timeout=60)

    while next_url:
        if response.status_code != 200:
            log.error(f"{api_name} API failed. Status Code: {response.status_code} url: {next_url}")
            next_url = None
        else:
            api_data = response.json()
            storage.extend(api_data.get("results", []))
            next_url = api_data['next']
            if next_url:
                response = requests.get(next_url)

    log.info(f"{api_name} API call complete. Rows pulled {len(storage)}")
    return pd.DataFrame(storage)

def to_database(df : pd.DataFrame, table_name : str):
    log.info(f"Starting database creation for {table_name}")
    ingest_df : pd.DataFrame = df.copy()
    #Note, this is AI generated code. This is used to capture standard time in UTC
    ingest_df["ingested_at_utc"] = datetime.utcnow().isoformat(timespec="seconds")

    with sqlite3.connect(PATH_DB) as conn:
        ingest_df.to_sql(table_name, conn, if_exists="replace", index=False)
        log.info(f"Table {table_name} has been created with {ingest_df.shape[0]} rows")

if __name__ == "__main__":
    log.info("Script has started")

    for key,item in url_dict.items():
        df = api_call(key,item)
        to_database(df,f"ipeds_raw_{key}")

    log.info("Script has ended successfully")


