import pandas as pd
import requests
import sys
import matplotlib.pyplot as plt
from utils.utils import Utils


class TeslaRevenueService:
    
    """Service to get the Tesla revenue."""

    URI = "https://ycharts.com/companies/TSLA/revenues"
    utils = Utils()

    def __init__(self):
        pass

    def download_html(self):
        """Download the HTML."""
        target = requests.get(self.URI, timeout=5, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
        if target.status_code == 200:
            print("Downloaded successfully")
        else:
            print("Failed to download")
            sys.exit(0)
        return target

    def find_quarterly_table(self, tables):
        """Find the table with the quarterly evolution."""
        for table in tables:
            if 'Net Income (Quarterly)' in str(table):
                return table
        return None
    
    def display_data(self, df):

        """Display the data."""
        
        df['Concept'] = df['Concept'].apply(lambda x: x.replace('(Quarterly)', ''))
        df['Figure'] = pd.to_numeric(df['Figure'], errors='coerce')
        df.plot(kind='bar', x='Concept', y='Figure', color='skyblue', width=0.8)
        plt.xticks(rotation=45)
        plt.ylabel('Millions of USD')
        plt.title('Tesla Quarterly Net Income')
        plt.show()

    def get_tesla_revenue(self):

        """Get the Tesla revenue."""

        quarterly_table = self.find_quarterly_table(self.utils.find_all_tables(self.download_html()))
        if quarterly_table is None:
            print("No quarterly table found")
            sys.exit(0)
        df = self.utils.convert_table_to_dataframe(quarterly_table)
        self.display_data(df)
        return df