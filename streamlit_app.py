import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def get_data():
    # Define the scopes for Google Sheets and Google Drive APIs
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    # Load the credentials from the service account file
    credentials = Credentials.from_service_account_file('service_account.json', scopes=scopes)

    # Authorize the credentials and create a client
    client = gspread.authorize(credentials)

    # Open the Google Spreadsheet
    spreadsheet = client.open("tesla")

    # Select the first sheet
    worksheet = spreadsheet.sheet1

    # Get the values from the spreadsheet
    values = worksheet.get_all_values()

    # Convert values to a Pandas DataFrame
    df = pd.DataFrame(values[1:], columns=values[0])

    return df

# Get the data
df = get_data()

# Convert date column to datetime type
df['priceDate'] = pd.to_datetime(df['priceDate'])

# Set the 'priceDate' column as the DataFrame index
df.set_index('priceDate', inplace=True)

# Convert numeric columns to appropriate data types
numeric_columns = ['close', 'high', 'low', 'open', 'volume']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

st.title("Historical Trend of Tesla (TSLA) Stock Closing and Opening Prices")

# Display the line chart using Streamlit
st.line_chart(df[['close', 'open']])  # Adjust the columns as per your preference
