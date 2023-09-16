# Jugaad_data (Indian market live)
# prettyTable to print data in tabular format
from jugaad_data.nse import NSELive
import pandas as pd

def color_positive_green(val):
    if val > 0:
        color = 'green'
    else:
        color = 'black'
    return 'color: %s' % color

# Initiate the connection
fno = NSELive().live_fno()
fno_data = fno['data']

# Initiate and Formulate the headers of the table
df = pd.DataFrame(columns=['SYMBOL', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'CHANGE%', 'CHANGE', 'INDUSTRY'])
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 600)

for fo in fno_data:

    symbol = fo['meta']['symbol']
    dayOpen = fo['open']
    dayClose = fo['lastPrice']
    high = fo['dayHigh']
    low = fo['dayLow']
    industry = fo['meta']['industry'] if 'industry' in fo['meta'] else 'NA'
    change = fo['change']
    p_change = fo['pChange']
    new_record = pd.DataFrame([{'SYMBOL': fo['meta']['symbol'],
                    'OPEN': float(fo['open']),
                    'HIGH': float(fo['dayHigh']),
                    'LOW': float(fo['dayLow']),
                    'CLOSE': float(fo['lastPrice']),
                    'CHANGE%': float((str(p_change)[0:7])),
                    'CHANGE': float((str(change)[0:7])),
                    'INDUSTRY': industry
                    }])

    df = pd.concat([df, new_record], ignore_index=True)

df = df.sort_values(by=['CHANGE%'], ascending=False)
df.to_excel('fno.xlsx', sheet_name='fno', engine='openpyxl', index=False)
print(df)
