from datetime import datetime
from jugaad_data.nse import NSELive
import pandas as pd

print('Enter the Symbol: ')
symbol = input()

months = { 1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "June", 7: "July", 8: "Aug",  9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec" }

stock_quote_fno_data = NSELive().stock_quote_fno(symbol)

def get_option(strike, option_type, expiry_date):
    stock_option_chain = stock_quote_fno_data['stocks']
    stock_option = None
    for option in stock_option_chain:
        metadata = option['metadata']
        if str(metadata['optionType']).casefold() == option_type.casefold() and metadata['strikePrice'] == strike and metadata['expiryDate'] == expiry_date:
            stock_option = option
    return stock_option

def get_earliest_expiry():
    expiry_dates = list(set(stock_quote_fno_data['expiryDatesByInstrument']['Stock Options']))
    earliest_expiry = None
    for date in expiry_dates:
        expiry_date = datetime.strptime(date, '%d-%b-%Y').date()
        if earliest_expiry is None:
            earliest_expiry = date
        earliest_expiry = date if datetime.strptime(earliest_expiry, '%d-%b-%Y').date() > expiry_date else earliest_expiry
    return earliest_expiry

def get_atm_strike():
    cmp = stock_quote_fno_data['underlyingValue']
    atm = strikes[0]
    for strike in strikes:
        if atm < strike <= cmp:
            atm = strike

    return atm

strikes = list(set(stock_quote_fno_data['strikePrices']))
earliest_expiry_date = get_earliest_expiry()

df = pd.DataFrame(columns=['EXPIRY', 'CALL-OI', 'CALL', 'STRIKE', 'PUT', 'PUT-OI'])
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 600)

for strike_price in strikes:
    if strike_price == 0:
        continue

    call_option = get_option(strike_price, 'call', earliest_expiry_date)
    put_option = get_option(strike_price, 'put', earliest_expiry_date)

    new_record = pd.DataFrame([{
                                'EXPIRY': earliest_expiry_date,
                                'CALL-OI': call_option['marketDeptOrderBook']['tradeInfo']['openInterest'],
                                'CALL': call_option['metadata']['lastPrice'],
                                'STRIKE': strike_price,
                                'PUT': put_option['metadata']['lastPrice'],
                                'PUT-OI': put_option['marketDeptOrderBook']['tradeInfo']['openInterest']
                                }])

    df = pd.concat([df, new_record], ignore_index=True)

df = df.sort_values(by=['STRIKE'], ascending=True)
print(df)