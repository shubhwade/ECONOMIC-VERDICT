import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from textblob import TextBlob

# 🟦 NewsAPI Key (replace with your own key)
NEWS_API_KEY = "1e47c84fee974dcfabb2445d2a4bd197"

# 🟪 News Fetch Function
def fetch_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])[:5]
    except Exception as e:
        st.warning(f"Could not fetch news: {e}")
        articles = []
    news_list = []
    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        text = f"{title}. {description}"
        sentiment_score = round(TextBlob(text).sentiment.polarity, 2) if text else 0
        news_list.append({
            "title": title,
            "description": description,
            "sentiment": sentiment_score,
            "url": article.get("url", ""),
            "source": article.get("source", {}).get("name", "")
        })
    return news_list

# 🟨 Sidebar Branding (visible everywhere)
sidebar_html = """
    <div style="margin-top:30px;text-align:center;">
      <span style="color:#EEEEEE;background:#2c2c2c;padding:6px 14px;border-radius:8px;font-size:16px;">
        Made by <b>Shubh Wade</b> 🚀
      </span>
    </div>
"""
st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)
st.sidebar.markdown("---")

# 🟧 Modern Tabs Navigation
tabs = st.tabs(["📊 Dashboard", "📰 Live News"])

# ==============================
# DASHBOARD TAB
# ==============================
with tabs[0]:
    st.title("📊 Economic Verdict - Stock Sentiment Analyzer")
    st.markdown(
        "Analyze the relationship between social media sentiment and stock performance. "
        "<br><i>Upload your final processed Excel or CSV to get started!</i>",
        unsafe_allow_html=True,
    )
    st.sidebar.title("Upload Data")
    uploaded_file = st.sidebar.file_uploader(
        "Choose FINAL_ECONOMIC_VERDICT_DATA.xlsx or .csv", type=["xlsx", "csv"])

    if uploaded_file:
        ext = uploaded_file.name.split('.')[-1]
        try:
            if ext == "xlsx":
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"⚠️ Could not open file: {e}")
            st.stop()

        REQUIRED_COLUMNS = [
            "Date", "Close", "Avg_Sentiment", "Price_Change_Pct", "Sentiment_Category"
        ]
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.error(
                f"⚠️ Uploaded file missing columns: <b>{', '.join(missing_cols)}</b>. "
                "Please check your exported data file!",
                unsafe_allow_html=True,
            )
        else:
            st.subheader("📈 Stock Price Trend")
            fig1 = px.line(df, x="Date", y="Close", title="Stock Closing Price Over Time")
            st.plotly_chart(fig1, use_container_width=True)

            st.subheader("😊 Sentiment Trend")
            fig2 = px.area(df, x="Date", y="Avg_Sentiment", title="Average Sentiment Over Time")
            st.plotly_chart(fig2, use_container_width=True)

            st.subheader("🔗 Sentiment vs Price Change (Correlation)")
            df_corr = df.dropna(subset=["Avg_Sentiment", "Price_Change_Pct"])
            if not df_corr.empty:
                fig3 = px.scatter(
                    df_corr, x="Avg_Sentiment", y="Price_Change_Pct",
                    trendline="ols", title="Sentiment vs. Price Change"
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info(
                    "No data available for the correlation plot. "
                    "Check if 'Avg_Sentiment' and 'Price_Change_Pct' have values.")

            st.subheader("📊 Sentiment Category Distribution")
            category_counts = df['Sentiment_Category'].value_counts().reset_index()
            category_counts.columns = ['Sentiment_Category', 'Count']
            fig4 = px.bar(
                category_counts, x="Sentiment_Category", y="Count",
                color="Sentiment_Category",
                title="Sentiment Category Breakdown"
            )
            st.plotly_chart(fig4, use_container_width=True)

            st.subheader("🗃️ Full Data Table")
            st.dataframe(df, use_container_width=True)

            st.sidebar.download_button(
                "Download Full Data as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="processed_economic_verdict_data.csv",
                mime="text/csv"
            )
    else:
        st.info("Upload your final processed Excel/CSV file using the sidebar to see results.")

# ==============================
# LIVE NEWS TAB
# ==============================
with tabs[1]:
    st.title("📰 Live News & Sentiment")
    st.markdown("Get latest headlines and real-time sentiment analysis for stocks, companies, or keywords.")

    col1, col2 = st.columns([2, 1])
    with col1:
        stock_query = st.text_input(
            "Search news for (Stock/Company/Keyword):", value="AAPL", help="Try stock tickers like AAPL, TSLA or company names.")
    with col2:
        show_news = st.button("Show News")

    if show_news:
        news_results = fetch_news(stock_query)
        if news_results:
            st.subheader(f"Results for '{stock_query}':")
            avg_sentiment = round(sum([item['sentiment'] for item in news_results]) / len(news_results), 2)
            st.markdown(
                f"<b>Average Sentiment:</b> "
                f"{'🟢 Positive' if avg_sentiment > 0 else ('🔴 Negative' if avg_sentiment < 0 else '🟡 Neutral')} ({avg_sentiment})",
                unsafe_allow_html=True,
            )
            for item in news_results:
                with st.expander(item['title']):
                    st.markdown(f"""
**Source:** {item['source']}  
**Sentiment:** {'🟢 Positive' if item['sentiment'] > 0 else ('🔴 Negative' if item['sentiment'] < 0 else '🟡 Neutral')} ({item['sentiment']})

{item['description']}

[Read full article]({item['url']})
""")
        else:
            st.warning("No news articles found, or NewsAPI request limit reached. Try again later.")
    else:
        st.info("Enter a keyword/ticker and click Show News for latest headlines.")

    footer_html = """
        <div style="margin-top:40px;text-align:center;">
          <span style="background:#EEEEEE;color:#444;padding:8px 18px;border-radius:13px;font-size:17px;">
            Made by <b>Shubh Wade</b> 🚀
          </span>
        </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

