import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

URI = "https://ycharts.com/companies/TSLA/revenues"


#Step 2: Download HTML
def download_html():
    target = requests.get(URI, timeout=5, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
    if target.status_code == 200:
        print("Downloaded successfully")
    else:
        print("Failed to download")
        sys.exit(0)
    return target

#Step 3: Transform the HTML
def find_all_tables(html):
    """Find all the tables.
    """
    soup = BeautifulSoup(html.text, 'html.parser')
    tables = soup.find_all('table')
    return tables

def find_quarterly_table(tables):
    """Find the table with the quarterly evolution."""
    for table in tables:
        if 'Net Income (Quarterly)' in str(table):
            print(table)
            return table
    return None


#Step 4: Process the DataFrame
def process_data(df):
    """
    Cleans the DataFrame by:
    - Replacing '$', commas, and spaces with NaN.
    - Dropping rows and columns that are entirely empty or contain only NaN.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to process.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df = df.replace({'\$': pd.NA, ',': pd.NA, ' ': pd.NA}, regex=True)
    df.dropna(inplace=True, axis=1, how='all')
    df.dropna(inplace=True, axis=0, how='all')
    return df


#Step 5: Store the data in sqlite
def save_dataframe_to_sqlite(df, db_name, table_name):
    """Save the DataFrame to a SQLite database.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        db_name (str): The name of the database.
        table_name (str): The name of the table.
    """
    try:
        conn = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
        sys.exit(0)
    df.to_sql(table_name, conn, if_exists='replace')
    conn.close()

#Step 6: Visualize the data
def display_data(df):
    """Display the data."""
    print(df.head())


def convert_table_to_dataframe(table):
    """Convert a BeautifulSoup table to a pandas DataFrame."""
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [item.text.strip() for item in cols]
        data.append([item for item in cols if item])
    
    df = pd.DataFrame(data,  columns=["Concept", "Figure"])
    return df

def main():
    """Main function."""
    quarterly_table = find_quarterly_table(find_all_tables(download_html()))
    if quarterly_table is None:
        print("No quarterly table found")
        sys.exit(0)
    display_data(convert_table_to_dataframe(quarterly_table))

if __name__ == "__main__":
    main()
    sys.exit(0)