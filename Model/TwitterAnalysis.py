import datetime as dt
import pandas as pd
import snscrape.modules.twitter as sntwitter
import traceback
try:
    from SentimentAnalyzer import analyze_sentiment
except:
    from Model.SentimentAnalyzer import analyze_sentiment

import warnings 
warnings.filterwarnings('ignore')

def get_tweets(ticker, current_date):
    try:
        noOfDays=1
        noOfTweets=100
        tomo = dt.datetime.now() + dt.timedelta(days = int(noOfDays))
        tomo = tomo.strftime('%Y-%m-%d')

        # Define the search query
        search_query = ticker + ' lang:en since:' +  current_date + ' until:' + tomo + ' -filter:links -filter:replies'
        # Scrape Twitter data
        tweets = []

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
            text = tweet.content
            tweets.append(text)

            if len(tweets) > noOfTweets:
                break
            
        return tweets

    except:
        print(traceback.print_exc())
        return []

def get_twitter_analysis(ticker):

    try:
        file_path = "C://Users/Rachel/Desktop/FP/Database/Datasets/" + ticker + '.csv'
        df = pd.read_csv(file_path)

        current_df = df.tail(1)
        current_date = list(current_df['date'])[0].split(" ")[0]
        tweets = get_tweets(ticker, current_date)

        # Creating Tweets DF
        tweets_df = pd.DataFrame()
        tweets_df["tweets"] = tweets

        tweets_df["compound_score"] = tweets_df['tweets'].apply(lambda x: analyze_sentiment(x)[0])
        tweets_df["sentiment"] = tweets_df['tweets'].apply(lambda x: analyze_sentiment(x)[1])
        
        overall_compound_score = (tweets_df["compound_score"].sum())/len(tweets_df)
        overall_sentiment = "Neutral"

        # Classify the sentiment based on the compound score
        if overall_compound_score >= 0.05:
            overall_sentiment = 'Positive'
        elif overall_compound_score <= -0.05:
            overall_sentiment = 'Negative'
        else:
            overall_sentiment = 'Neutral'

        return tweets_df, overall_compound_score, overall_sentiment

    except:
        print(traceback.print_exc())
        return pd.DataFrame(), 0, ""
    
"""
tweets_df, overall_compound_score, overall_sentiment = get_twitter_analysis(ticker="NVDA")
print("overall_compound_score: ", overall_compound_score)
print("overall_compound_score: ", overall_compound_score)
print(tweets_df.head())

count_df = pd.DataFrame(tweets_df.value_counts())
print(count_df)
"""

