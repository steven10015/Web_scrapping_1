import numpy as np
import pandas as pd
import sqlite3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Download the data using request library
url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

# Parse the html data using beautiful_soup
page_soup = soup(webpage, 'html.parser')

tables = page_soup.find('div', {'id': 'style-1'})  # find all the tables

data = []
for row in tables.find_all('tr'):
    row_data = []
    for cell in row.find_all('td'):
        row_data.append(cell.text)
    data.append(row_data)

df = pd.DataFrame(data, columns=['Date', 'Revenue'])  # create the dataframe
# find table with Tesla quarterly revenue
find_table = df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
tesla_quartely_revenue = find_table.reset_index(drop=True)
tesla_quartely_revenue['Revenue'] = tesla_quartely_revenue['Revenue'].str.replace(
    "$", "", regex=True).str.replace(",", "", regex=True)  # Remove the $ and replace "," to "."

# remove empty rows or nan
tesla_revenue = tesla_quartely_revenue[tesla_quartely_revenue['Revenue'] != ""].reset_index(
    drop=True)
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].astype(int)

# convert the df in a list of tuplets
tesla_revenue_records = tesla_revenue.to_records(index=False)
tesla_revenue_lot = list(tesla_revenue_records)

# conect to sqlite3
conn = sqlite3.connect('Tesla.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS teslarevenue
             (Date, Revenue)''')

# insert the rows
c.executemany('INSERT INTO teslarevenue VALUES (?,?)', tesla_revenue_lot)

# Save (commit) the changes
conn.commit()

# Vizualize the data
dates = tesla_revenue["Date"]
x = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
y = tesla_revenue["Revenue"]

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=500))
plt.yticks(np.arange(min(y), max(y)+1, 2000))
plt.plot(x, y)
plt.gcf().autofmt_xdate()
plt.show()