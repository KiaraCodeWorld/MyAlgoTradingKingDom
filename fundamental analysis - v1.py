import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

def get_fundamental_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        fundamentals = {
            'Symbol': ticker,
            'Name': info.get('longName', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'EPS': info.get('trailingEps', 'N/A'),
            'Dividend Yield': info.get('dividendYield', 'N/A'),
            'Book Value': info.get('bookValue', 'N/A'),
            'Price to Book': info.get('priceToBook', 'N/A'),
            'Debt to Equity': info.get('debtToEquity', 'N/A')
        }
        
        return fundamentals
    except Exception as e:
        print(f"Error fetching fundamental data for {ticker}: {str(e)}")
        return {key: 'Error' for key in ['Symbol', 'Name', 'Sector', 'Market Cap', 'P/E Ratio', 'EPS', 'Dividend Yield', 'Book Value', 'Price to Book', 'Debt to Equity']}

def calculate_intrinsic_value(ticker):
    try:
        stock = yf.Ticker(ticker)
        
        free_cash_flow = stock.info.get('freeCashflow', 0)
        shares_outstanding = stock.info.get('sharesOutstanding', 0)
        
        growth_rate = 0.05
        discount_rate = 0.10
        
        fcf_per_share = free_cash_flow / shares_outstanding if shares_outstanding != 0 else 0
        intrinsic_value = fcf_per_share * (1 + growth_rate) / (discount_rate - growth_rate)
        
        return round(intrinsic_value, 2)
    except Exception as e:
        print(f"Error calculating intrinsic value for {ticker}: {str(e)}")
        return 'Error'

def get_analyst_ratings(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/{ticker}?apikey=YOUR_FMP_API_KEY"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        if data:
            latest_rating = data[0]
            return {
                'Buy': latest_rating.get('buyRecommendation', 'N/A'),
                'Hold': latest_rating.get('holdRecommendation', 'N/A'),
                'Sell': latest_rating.get('sellRecommendation', 'N/A'),
                'Strong Buy': latest_rating.get('strongBuyRecommendation', 'N/A'),
                'Strong Sell': latest_rating.get('strongSellRecommendation', 'N/A')
            }
        else:
            return {'Error': 'No analyst ratings available'}
    except requests.RequestException as e:
        print(f"Error fetching analyst ratings for {ticker}: {str(e)}")
        return {'Error': 'Failed to fetch analyst ratings'}

def stock_scanner(stock_list):
    results = []
    
    for ticker in stock_list:
        try:
            fundamentals = get_fundamental_data(ticker)
            intrinsic_value = calculate_intrinsic_value(ticker)
            analyst_ratings = 'buy' #get_analyst_ratings(ticker)
            
            stock_data = {**fundamentals, 'Intrinsic Value': intrinsic_value, 'Analyst Ratings': analyst_ratings}
            results.append(stock_data)
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            error_data = {
                'Symbol': ticker,
                'Name': 'Error',
                'Sector': 'Error',
                'Market Cap': 'Error',
                'P/E Ratio': 'Error',
                'EPS': 'Error',
                'Dividend Yield': 'Error',
                'Book Value': 'Error',
                'Price to Book': 'Error',
                'Debt to Equity': 'Error',
                'Intrinsic Value': 'Error',
                'Analyst Ratings': {'Error': 'Failed to process'}
            }
            results.append(error_data)
    
    return pd.DataFrame(results)

# Example usage
stock_list = ['GB', 'SOFI', 'KORE', 'SES', 'ASMB']
try:
    scanner_results = stock_scanner(stock_list)
    print(scanner_results)
except Exception as e:
    print(f"An error occurred while running the stock scanner: {str(e)}")