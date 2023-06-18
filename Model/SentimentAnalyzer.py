from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import traceback

def analyze_sentiment(tweet):
    try:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(tweet)
        
        # Extract the compound score, which represents the overall sentiment
        compound_score = sentiment_scores['compound']
        
        # Classify the sentiment based on the compound score
        if compound_score >= 0.05:
            sentiment = 'Positive'
        elif compound_score <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return compound_score, sentiment, 1

    except:
        print(traceback.print_exc())
        return "", "", -2