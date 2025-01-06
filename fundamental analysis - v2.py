import yfinance as yf
#from newsapi import NewsApiClient
import pandas as pd

# Initialize NewsAPI client (replace 'YOUR_NEWSAPI_KEY' with your actual API key)
#newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY')

# List of stock tickers
stock_list = ['AAPL', 'MSFT', 'GOOGL']  # Replace with your list of stocks

for ticker in stock_list:
    print(f"Fetching data for {ticker}...\n")
    stock = yf.Ticker(ticker)
    
    # Fetch company info
    info = stock.info

    # Company description
    company_name = info.get('longName', 'N/A')
    description = info.get('longBusinessSummary', 'N/A')

    # Current trading price
    current_price = info.get('currentPrice', 'N/A')

    # Fundamental data
    pe_ratio = info.get('trailingPE', 'N/A')
    eps = info.get('trailingEps', 'N/A')
    market_cap = info.get('marketCap', 'N/A')
    dividend_yield = info.get('dividendYield', 'N/A')
    beta = info.get('beta', 'N/A')
    book_value_per_share = info.get('bookValue', 'N/A')

    # Analyst ratings
    try:
        recommendations = stock.recommendations
        if not recommendations.empty:
            latest_rec = recommendations.iloc[-1]
            analyst_rating = latest_rec['To Grade']
        else:
            analyst_rating = 'N/A'
    except:
        analyst_rating = 'N/A'

    # Intrinsic value estimation (Using Graham Number)
    if (eps != 'N/A') and (book_value_per_share != 'N/A'):
        try:
            graham_number = (22.5 * eps * book_value_per_share) ** 0.5
            graham_number = round(graham_number, 2)
        except:
            graham_number = 'N/A'
    else:
        graham_number = 'N/A'

    # Fetch news articles
    news_list = []
    try:
        news_articles = newsapi.get_everything(q=company_name,
                                               language='en',
                                               sort_by='relevancy',
                                               page_size=5)
        news_list = news_articles['articles']
    except Exception as e:
        print(f"Error fetching news: {e}")

    # Display the data
    print(f"Company: {company_name}")
    print(f"Description: {description}\n")
    print(f"Current Price: {current_price}")
    print(f"P/E Ratio: {pe_ratio}")
    print(f"Earnings Per Share (EPS): {eps}")
    print(f"Market Cap: {market_cap}")
    print(f"Dividend Yield: {dividend_yield}")
    print(f"Beta: {beta}")
    print(f"Analyst Rating: {analyst_rating}")
    print(f"Estimated Intrinsic Value (Graham Number): {graham_number}\n")

    ticker = yf.Ticker(ticker)
    news = ticker.news
    print("Title: " , news[0]['content']['title'])
    print("Summary: " , news[0]['content']['summary'])    

    print("Recent News:")
    if news_list:
        for article in news_list:
            title = article['title']
            url = article['url']
            published_at = article['publishedAt']
            print(f"- {title} ({published_at})")
            print(f"  {url}\n")
    else:
        print("No recent news found.\n")

    print("="*80 + "\n")