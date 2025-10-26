import pandas as pd
import numpy as np
from stockfetcher import fetch_stock_data
from sentimentanalyzer import generate_sentiment_data

def create_integrated_dataset(ticker, start_date, end_date):
    """
    Combine stock data with sentiment data for comprehensive analysis
    
    Returns:
    DataFrame: Merged dataset with correlations
    """
    print(f"\n{'='*50}")
    print(f"Creating Integrated Dataset for {ticker}")
    print(f"{'='*50}\n")
    
    # Fetch both datasets
    stock_df = fetch_stock_data(ticker, start_date, end_date)
    sentiment_df = generate_sentiment_data(ticker, start_date, end_date)
    
    # Ensure Date columns are datetime
    stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.date
    sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date']).dt.date
    
    # Merge on Date
    merged_df = pd.merge(stock_df, sentiment_df, on='Date', how='inner')
    
    # Calculate additional metrics
    merged_df['Sentiment_Category'] = merged_df['Avg_Sentiment'].apply(
        lambda x: 'Positive' if x > 0.1 else ('Negative' if x < -0.1 else 'Neutral')
    )
    
    # Calculate correlation between sentiment and price change
    correlation = merged_df['Avg_Sentiment'].corr(merged_df['Price_Change_Pct'])
    
    print(f"\n{'='*50}")
    print(f"KEY METRICS")
    print(f"{'='*50}")
    print(f"Total Days Analyzed: {len(merged_df)}")
    print(f"Average Sentiment Score: {merged_df['Avg_Sentiment'].mean():.4f}")
    print(f"Average Price Change: {merged_df['Price_Change_Pct'].mean():.2f}%")
    print(f"Sentiment-Price Correlation: {correlation:.4f}")
    print(f"\nPositive Days: {len(merged_df[merged_df['Sentiment_Category']=='Positive'])}")
    print(f"Negative Days: {len(merged_df[merged_df['Sentiment_Category']=='Negative'])}")
    print(f"Neutral Days: {len(merged_df[merged_df['Sentiment_Category']=='Neutral'])}")
    print(f"{'='*50}\n")
    
    return merged_df, correlation

# Main execution
if __name__ == "__main__":
    # Create integrated dataset
    final_data, correlation = create_integrated_dataset("AAPL", "2024-01-01", "2024-10-25")
    
    # Save for Tableau and Power BI
    final_data.to_excel("FINAL_ECONOMIC_VERDICT_DATA.xlsx", index=False)
    final_data.to_csv("FINAL_ECONOMIC_VERDICT_DATA.csv", index=False)
    
    print("✅ Files saved:")
    print("   - FINAL_ECONOMIC_VERDICT_DATA.xlsx (for Power BI)")
    print("   - FINAL_ECONOMIC_VERDICT_DATA.csv (for Tableau)")
    print("\n🎉 Data preparation complete!")

