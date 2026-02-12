import requests
import pandas as pd
import sqlite3
from datetime import datetime

DB_PATH = "higher_ed.db"

def fetch_all_pages(url: str, timeout: int = 60) -> pd.DataFrame:
    """Fetch all paginated results from Urban Institute API"""
    rows = []
    next_url = url

    while next_url:
        print("Pulling:", next_url)
        r = requests.get(next_url, timeout=timeout)
        r.raise_for_status()
        payload = r.json()

        rows.extend(payload.get("results", []))
        next_url = payload.get("next")

    df = pd.DataFrame(rows)
    return df

def write_raw(df: pd.DataFrame, table_name: str):
    """Write dataframe to SQLite as raw table"""
    df = df.copy()
    df["ingested_at_utc"] = datetime.utcnow().isoformat(timespec="seconds")

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Table written: {table_name} ({len(df)} rows)")

def main():
    year = 2021

    directory_url = f"https://educationdata.urban.org/api/v1/college-university/ipeds/directory/{year}/"
    tuition_url   = f"https://educationdata.urban.org/api/v1/college-university/ipeds/academic-year-tuition/{year}/"

    print("Pulling directory data...")
    df_directory = fetch_all_pages(directory_url)

    print("Pulling tuition data...")
    df_tuition = fetch_all_pages(tuition_url)

    print("Writing to SQLite...")
    write_raw(df_directory, f"raw_ipeds_directory_{year}")
    write_raw(df_tuition, f"raw_ipeds_ay_tuition_{year}")

    print("\nSUCCESS: Raw data warehouse created → higher_ed.db")

if __name__ == "__main__":
    main()
