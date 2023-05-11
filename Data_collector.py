import pandas as pd
import requests
import csv

# Replace YOUR_API_KEY with your Alpha Vantage API key
api_key = '0CKGI68VCNYYAWSR'

# Set the stock symbol and interval
symbol = 'TQQQ'
interval = '5min'

# Set the time period for the data
time_period = 'year1month1'

# Make the API request
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&interval={interval}&apikey={api_key}&slice={time_period}'
response = requests.get(url)
print(response)

response_data = b'time,open,high,low,close,volume\r\n2023-04-21 20:00:00,26.815,26.82,26.8,26.8099,56108\r\n'

lines = response.content.decode().splitlines()

# Create a CSV writer object
csv_writer = csv.writer(open('output.csv', 'w'), delimiter=',')

# Write the header row
csv_writer.writerow(['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

# Write each row to the CSV file
for line in lines[1:]:
    row = line.split(',')
    # Split the date and time into separate columns and write them with a comma separator
    date_time = row[0].split(' ')
    row[0:1] = row[0].replace(' ', ',')
    csv_writer.writerow(row)
