from textblob import TextBlob
import pandas as pd
import numpy as np

def generate_sentiment_data(ticker, start_date, end_date):
    """
    Generate synthetic social media sentiment data for stock analysis
    
    Parameters:
    ticker (str): Stock symbol
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
    DataFrame: Daily sentiment scores and metrics
    """
    # Create date range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Sample social media posts (simulate real tweets/posts)
    positive_posts = [
        f"{ticker} showing strong growth! Great buy opportunity.",
        f"Bullish on {ticker}. Earnings exceeded expectations!",
        f"Love this company. {ticker} stock is going to the moon!",
        f"{ticker} released amazing product. Stock will surge.",
        f"Analysts upgraded {ticker}. Very positive outlook."
    ]
    
    neutral_posts = [
        f"{ticker} stock moving sideways. Wait and see.",
        f"No major news on {ticker} today. Holding steady.",
        f"{ticker} quarterly report was as expected.",
        f"Market conditions affecting {ticker} like others."
    ]
    
    negative_posts = [
        f"{ticker} missed revenue targets. Concerning trend.",
        f"Bearish on {ticker}. Too much competition.",
        f"{ticker} facing regulatory issues. Selling my shares.",
        f"Disappointed with {ticker} management decisions.",
        f"{ticker} stock overvalued. Time to sell."
    ]
    
    all_posts = positive_posts + neutral_posts + negative_posts
    
    sentiment_data = []
    
    for date in dates:
        # Random number of posts per day (50-200)
        num_posts = np.random.randint(50, 200)
        daily_sentiments = []
        
        for _ in range(num_posts):
            # Randomly select a post
            post = np.random.choice(all_posts)
            
            # Analyze sentiment using TextBlob
            blob = TextBlob(post)
            sentiment_score = blob.sentiment.polarity  # -1 to 1
            daily_sentiments.append(sentiment_score)
        
        # Calculate daily metrics
        avg_sentiment = np.mean(daily_sentiments)
        max_sentiment = np.max(daily_sentiments)
        min_sentiment = np.min(daily_sentiments)
        
        positive_count = len([s for s in daily_sentiments if s > 0.1])
        negative_count = len([s for s in daily_sentiments if s < -0.1])
        neutral_count = num_posts - positive_count - negative_count
        
        sentiment_data.append({
            'Date': date,
            'Avg_Sentiment': round(avg_sentiment, 4),
            'Max_Sentiment': round(max_sentiment, 4),
            'Min_Sentiment': round(min_sentiment, 4),
            'Post_Count': num_posts,
            'Positive_Posts': positive_count,
            'Negative_Posts': negative_count,
            'Neutral_Posts': neutral_count,
            'Positive_Ratio': round(positive_count / num_posts, 4),
            'Negative_Ratio': round(negative_count / num_posts, 4)
        })
    
    df = pd.DataFrame(sentiment_data)
    print(f"Generated sentiment data for {len(df)} days")
    return df

# Test the function
if __name__ == "__main__":
    sentiment_data = generate_sentiment_data("AAPL", "2024-01-01", "2024-10-25")
    print("\nFirst 5 rows:")
    print(sentiment_data.head())
    
    print("\nSentiment statistics:")
    print(sentiment_data['Avg_Sentiment'].describe())
    
    # Save to Excel
    sentiment_data.to_excel("sentiment_data_apple.xlsx", index=False)
    print("\nData saved to sentiment_data_apple.xlsx")
