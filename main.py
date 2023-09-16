from jugaad_data.nse import NSELive
import json
from prettytable import PrettyTable

stock = 'HAL'

n = NSELive().stock_quote(stock)

currentTrend = 'Bullish' if n['priceInfo']['open'] < n['priceInfo']['close'] else 'Bearish'
change = str(n['priceInfo']['close'] - n['priceInfo']['open'])[0:7]

currentTrend = f'{currentTrend} ({change})'

# Initiate and Formulate the headers of the table
table = PrettyTable(['SYMBOL', 'Industry', 'Prev close', 'CMP', 'Day\'s trend', 'ListingDate'])
table.add_row([n['info']['symbol'], n['industryInfo']['sector'], n['priceInfo']['previousClose'], n['priceInfo']['lastPrice'], currentTrend, n['metadata']['listingDate']])

print(table)

#pretty_json = json.dumps(n, indent=4)
#print(pretty_json)