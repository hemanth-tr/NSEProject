# Jugaad_data (Indian market live)
# prettyTable to print data in tabular format
from jugaad_data.nse import NSELive
import pandas as pd

# colors
green = "\033[1;32m%s\033[0m"
red = "\033[1;31m%s\033[0m"

# returns string in green
def positive_change(change):
    return green %str(change)[0:7]

# returns string in red
def negative_change(change):
    return red %str(change)[0:7]


# Initiate the connection
n = NSELive()

# Get the all the indices from the market
all_indices = n.all_indices()['data']

df = pd.DataFrame(columns=['SYMBOL', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'CHANGE', 'ADVANCES', 'DECLINES', 'UNCHANGED'])
for index in all_indices:
    advances = index['advances'] if 'advances' in index else None
    declines = index['declines'] if 'declines' in index else None
    unchanged = index['unchanged'] if 'unchanged' in index else None

    if advances is None or declines is None or unchanged is None:
        continue

    change = index['last'] - index['open']
    new_record = pd.DataFrame([{'SYMBOL': index['indexSymbol'],
                    'OPEN': float(index['open']),
                    'HIGH': float(index['high']),
                    'LOW': float(index['low']),
                    'CLOSE': float(index['last']),
                    'CHANGE': float((str(change)[0:7])),
                    'ADVANCES': float(advances),
                    'DECLINES': float(declines),
                    'UNCHANGED': float(unchanged),
                    }])

    df = pd.concat([df, new_record], ignore_index=True)

df = df.sort_values(by=['CHANGE'], ascending=False)
df.to_excel('indices.xlsx', sheet_name='indices', engine='openpyxl', index=False)
print(df.to_string())