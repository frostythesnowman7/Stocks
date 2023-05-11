import json
import requests
import datetime
import time

API_URL = "https://www.alphavantage.co/query"
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

###open config.json file and load params from config dictionary###
def get_config():
    ###Reads the configuration from the config.json file.###
    with open('config.json') as f:
        config = json.load(f)
    return config


def send_update(message, api_token, user_key):
    ###Sends a Pushover notification with the stock data to the specified user.###

    payload = {
        "token": api_token,
        "user": user_key,
        "message": message
    }
    response = requests.post(PUSHOVER_API_URL, data=payload)
    if response.status_code == 200:
        print(f"Notification sent successfully")
    else:
        print(f"Error sending notification")


def get_realtime_value(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Extract the current ticker value from the response
        ticker_value = data['chart']['result'][0]['meta']['regularMarketPrice']
        
        return ticker_value
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def closing_price(api_key, symbol):
    OUTPUT_SIZE = 'compact' # or 'full'
#    print('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize={OUTPUT_SIZE}&apikey={api_key}')
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize={OUTPUT_SIZE}&apikey={api_key}')
#    print(response.status_code)
    if response.status_code == 200:
        data = response.json()['Time Series (Daily)']
        yesterday = list(data.keys())[1]
        closing_price = data[yesterday]['4. close']
        return closing_price
    else:
        print("Error fetching data from Alpha Vantage API.")

###open config.json file and load params from config dictionary###
def main():
    config = get_config()
    api_key = config['api_key']
    symbols = config['symbols']
    api_token = config['pushover_api_token']
    user_key = config['pushover_user_key']


#check if its time to send an update and if its a weekday
    while True:
        for symbol in symbols:
        # Get the closing price and set the alert price if its the morning time
            if datetime.datetime.now().time() >= datetime.time(7, 30) and datetime.datetime.now().time() < datetime.time(23, 45) and datetime.datetime.today().weekday() < 5:
                closing_price_value = float(closing_price(api_key, symbol))
                alert_low = closing_price_value*.98
                alert_high = closing_price_value*1.02
                
        # Get the current price and send alerts, change alert price if triggered
            if datetime.datetime.now().time() >= datetime.time(2, 35) and datetime.datetime.now().time() < datetime.time(23, 45) and datetime.datetime.today().weekday() < 5:
                recent_data = float(get_realtime_value(symbol))
                if recent_data > alert_high:
                    message = symbol + r' is up 2%' 
                    send_update(message, api_token, user_key)
                    alert_low = recent_data*.98
                    alert_high = recent_data*1.02
                if recent_data < alert_low:
                    message = symbol + r' is down 2%' 
                    send_update(message, api_token, user_key)
                    alert_low = recent_data*.98
                    alert_high = recent_data*1.02

        time.sleep(60)


if __name__ == '__main__':
    main()
