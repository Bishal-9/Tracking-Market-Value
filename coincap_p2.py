import os
import requests
import datetime
import time
from gtts import gTTS

convert = 'INR'

listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=' + convert

request = requests.get(url=listings_url, headers={'X-CMC_PRO_API_KEY': 'Your_API_Key'})
result = request.json()
data = result['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

print()
print('ALERTS TRACKING...')
print()

already_hit_symbols = []

while True:
    with open('alerts.txt') as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()

            ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=' + ticker + '&convert=' + convert

            request = requests.get(url=ticker_url, headers={'X-CMC_PRO_API_KEY': 'Your_API_Key'})
            results = request.json()

            currency = results['data'][ticker]
            name = currency['name']
            last_updated = currency['last_updated']
            symbol = currency['symbol']
            quotes = currency['quote'][convert]
            price = quotes['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                text = name + ' hit ' + amount
                output = gTTS(text=text, lang='en', slow=False)
                output.save('alert.mp3')
                os.system('start alert.mp3')

                last_updated_string = datetime.datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")
                print(name + ' hit ' + amount + ' on ' + str(last_updated_string) + 'GST')
                already_hit_symbols.append(symbol)

    print('...')
    time.sleep(300)
