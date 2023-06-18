import feedparser
import traceback
import pandas as pd
import datetime as dt
import requests

try:
    from SentimentAnalyzer import analyze_sentiment
except:
    from Model.SentimentAnalyzer import analyze_sentiment

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

def convert_date_format(date_string):
    input_format = "%a, %d %b %Y %H:%M:%S %z"
    output_format = "%Y-%m-%d"

    # Convert the string to a datetime object
    datetime_obj = dt.datetime.strptime(date_string, input_format)

    # Convert the datetime object to the desired format
    formatted_date = datetime_obj.strftime(output_format)
    return formatted_date

def get_news_from_yahoo_finance(ticker, current_date):

    try:
        rssfeedurl = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%s&region=US&lang=en-US'%ticker
        NewsFeed = feedparser.parse(rssfeedurl)
        news_list = []

        for feed in NewsFeed.entries:
            date_string = feed['published']
            date = convert_date_format(date_string)

            if date == current_date:
                news_list.append(feed["summary"])

        return news_list
    
    except:
        print(traceback.print_exc())
        return []

def get_news_from_alphavantage(ticker, year, month, day):

    try:
        time_from = year + month + day + 'T0000'
        time_to   = year + month + day + 'T2359'
        url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={0}&time_from={1}&time_from={2}&limit=200&apikey=N0UE2A3TWI2VB058'.format(ticker, time_from, time_to)
        r = requests.get(url)
        data = r.json()

        news_list = []
        if "items" in data:
            for feed in data['feed']:
                news_list.append(feed['title'])
            return news_list
        
        else:
            return []
    except:
        print(traceback.print_exc())
        return []
    
def get_news_analysis(ticker):
    try:
        file_path = "C://Users/Rachel/Desktop/FP/Database/Datasets/" + ticker + '.csv'
        df = pd.read_csv(file_path)

        current_df = df.tail(1)
        current_date = list(current_df['date'])[0].split(" ")[0]

        news_1 = get_news_from_yahoo_finance(ticker, current_date)
        news_2 = get_news_from_alphavantage(ticker, year=current_date.split("-")[0], month=current_date.split("-")[1], day=current_date.split("-")[2])

        news = news_1 + news_2
        # Creating Tweets DF
        news_df = pd.DataFrame()
        news_df["news"] = news

        news_df["compound_score"] = news_df['news'].apply(lambda x: analyze_sentiment(x)[0])
        news_df["sentiment"] = news_df['news'].apply(lambda x: analyze_sentiment(x)[1])
        
        overall_compound_score = (news_df["compound_score"].sum())/len(news_df)
        overall_sentiment = "Neutral"

        # Classify the sentiment based on the compound score
        if overall_compound_score >= 0.05:
            overall_sentiment = 'Positive'
        elif overall_compound_score <= -0.05:
            overall_sentiment = 'Negative'
        else:
            overall_sentiment = 'Neutral'

        return news_df, overall_compound_score, overall_sentiment

    except:
        print(traceback.print_exc())
        return pd.DataFrame(), 0, ""

"""
news_df, overall_compound_score, overall_sentiment = get_news_analysis(ticker="AAPL")
print("overall_compound_score: ", overall_compound_score)
print("overall_sentiment: ", overall_sentiment)
print(news_df)
"""
