import yfinance as yf
import pandas as pd
import numpy as np

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data from Yahoo Finance
    
    Parameters:
    ticker (str): Stock symbol (e.g., 'AAPL', 'TSLA')
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
    DataFrame: Stock price data with Date, Open, High, Low, Close, Volume
    """
    print(f"Fetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    
    # Reset index to make Date a column
    df = df.reset_index()
    
    # Keep only necessary columns
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Calculate daily price change percentage
    df['Price_Change_Pct'] = df['Close'].pct_change() * 100
    
    # Calculate 7-day moving average
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    
    print(f"Successfully fetched {len(df)} days of data")
    return df

# Test the function
if __name__ == "__main__":
    # Fetch Apple stock data for 2024
    apple_data = fetch_stock_data("AAPL", "2024-01-01", "2024-10-25")
    print("\nFirst 5 rows:")
    print(apple_data.head())
    
    print("\nBasic statistics:")
    print(apple_data['Close'].describe())
    
    # Save to Excel for Tableau/Power BI
    apple_data.to_excel("stock_data_apple.xlsx", index=False)
    print("\nData saved to stock_data_apple.xlsx")
