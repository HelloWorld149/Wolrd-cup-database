import pandas as pd
from datetime import datetime

# Load the CSV file into a DataFrame
df = pd.read_csv('C:\\Users\\yunhu\\CS\\CS348\\WorldCup\\Database\\WorldCupMatches.csv')

# Define a function to convert the string format into a proper datetime format
def convert_datetime(s):
    if not isinstance(s, str):
        print(f"Non-string value encountered: {s}")
        return s  # or return a default datetime if you prefer
    
    # List of potential formats
    formats = ['%d %B %Y - %H:%M', '%d %b %Y - %H:%M']
    
    for fmt in formats:
        try:
            return datetime.strptime(s.strip(), fmt).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass  # move on to the next format

    # If none of the formats match
    print(f"Failed to convert: {s}")
    return s

# Apply the conversion function to the column that contains the datetime strings
df['_Datetime'] = df['_Datetime'].apply(convert_datetime)

# Save the DataFrame to a new CSV file
df.to_csv('C:\\Users\\yunhu\\CS\\CS348\\WorldCup\\Database\\WorldCupMatches_modified.csv', index=False)
