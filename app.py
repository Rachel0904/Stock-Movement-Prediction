# Importing Required Libraries
import joblib
import pickle
import streamlit as st
from annotated_text import annotated_text
import plotly.express as px
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards

# Database
from Database.functions import DATABASE
database = DATABASE()

# Configs
from Config import top_25_tickers
from Config.technical_indicators import technical_indicators

# Models
from Model.Williams_R import get_williams_r
from Model.TwitterAnalysis import get_twitter_analysis
from Model.NewsHeadlinesAnalysis import get_news_analysis

tickers_dict = top_25_tickers.tickers_dict
tickers_list = list(tickers_dict.keys())

def predict(ticker_selected, current_day_data):
    # Loading Scaler
    scaled_file_path = "C://Users/Rachel/Desktop/FP/Model/Scaler/" + ticker_selected
    ct1 = joblib.load(scaled_file_path)
    current_day_data = current_day_data[technical_indicators].copy()
    scaled_processed = ct1.transform(current_day_data)
    model_file_path = "https://github.com/Rachel0904/Stock-Movement-Prediction/Model/Model_Pickle/" + ticker_selected + '.pkl'
    model = pickle.load(open(model_file_path, 'rb'))
    prediction = model.predict(scaled_processed)
    return prediction[0]

def main():
    st.set_page_config(page_title="Stock Market Movement Prediction")

    st.title("STOCK MARKET ANALYSIS")
    st.sidebar.header('TOP 25 U.S BY MARKET CAP')
    ticker_selected = st.sidebar.selectbox('Select a Ticker', tickers_list)
    button_selected = st.sidebar.button(':red[ANALYZE]')

    if button_selected:
        st.header("Stock Market Analysis of {}".format(tickers_dict[ticker_selected]))

        column_1, column_2 = st.columns(2)

        # ML Model
        current_day_data = database.get_current_day_data(ticker_selected)
        prediction_class = predict(ticker_selected, current_day_data)
        with column_1:
            st.subheader("AI Model Prediction")
            if prediction_class == 0:
                st.metric(label="STOCK MOVEMENT DIRECTION", value="DOWN", delta="-0")
                style_metric_cards()
            else:
                st.metric(label="STOCK MOVEMENT DIRECTION", value="UP", delta="+1")
                style_metric_cards()
            add_vertical_space(8)
        if prediction_class == 1:
            model_1_prediction = 1
        else:
            model_1_prediction = -1

        # William's %R Buy/Sell Strategy
        with column_2:
            indicator_1, indicator_2, indicator_3 = get_williams_r(ticker_selected)
            st.subheader("William's %R")

            st.metric(label="Overbought/Oversold Condition Check", value=indicator_1, delta=None)
            print("indicator_3: ", indicator_3, type(indicator_3))
            st.metric(label="Trend Analysis", value=indicator_2, delta=indicator_3)
            style_metric_cards()
            add_vertical_space(2)

        with column_1:
            # Twitter Sentiment Analysis
            st.subheader("TWEET ANALYSIS")
            tweets_df, overall_compound_score, overall_sentiment = get_twitter_analysis(ticker=ticker_selected)
            
            if overall_sentiment == "Positive":
                model_2_prediction = 1
            elif overall_sentiment == 'Negative':
                model_2_prediction = -1
            else:
                model_2_prediction = 0

            count_df = pd.DataFrame(tweets_df["sentiment"].value_counts())
            count_df.reset_index(inplace=True)
            count_df.columns = ["Label", "Count"]

            st.caption("OVERALL")
            tweets_df.columns = ["TWEETS", "COMPOUND SCORE", "SENTIMENT"]
            annotated_text((str(overall_compound_score), "Overall Sentiment Score"))
            annotated_text((overall_sentiment, "Overall Sentiment"))

            column_1_tab_1, column_1_tab_2 = st.tabs(["Sentiment+Distribution", "Tweets+Sentiment"])

            with column_1_tab_1:
                fig = px.pie(count_df, values='Count',names="Label")
                st.plotly_chart(fig, use_container_width=True)

            with column_1_tab_2:
                st.dataframe(tweets_df, use_container_width=True)

        with column_2:
            # News Sentiment Analysis
            st.subheader("NEWS ANALYSIS")
            news_df, overall_compound_score, overall_sentiment = get_news_analysis(ticker=ticker_selected)
            
            if overall_sentiment == "Positive":
                model_3_prediction = 1
            elif overall_sentiment == 'Negative':
                model_3_prediction = -1
            else:
                model_3_prediction = 0

            count_df = pd.DataFrame(news_df["sentiment"].value_counts())
            count_df.reset_index(inplace=True)
            count_df.columns = ["Label", "Count"]

            news_df.columns = ["NEWSHEADLINES", "COMPOUND SCORE", "SENTIMENT"]

            st.caption("OVERALL")
            annotated_text((str(overall_compound_score), "Overall Sentiment Score"))
            annotated_text((overall_sentiment, "Overall Sentiment"))

            column_2_tab_1, column_2_tab_2 = st.tabs(["Sentiment+Distribution", "NewsHeadlines+Sentiment"])

            with column_2_tab_1:
                fig = px.pie(count_df, values='Count',names="Label")
                st.plotly_chart(fig, use_container_width=True)

            with column_2_tab_2:
                st.dataframe(news_df, use_container_width=True)

        #FinalOutput = (Weight1 * Model1) + (Weight2 * Model2) + (Weight3 * Model3)

        final_output = (0.2*model_1_prediction) + (0.4 * model_2_prediction) + (0.4 * model_3_prediction)
        if final_output > 0:
            final_value = "UP"
            st.sidebar.metric(label="OVERALL MOVEMENT", value=final_value)
            style_metric_cards()
        elif final_output == 0:
            final_value = "NEUTRAL"
            st.sidebar.metric(label="OVERALL MOVEMENT", value=final_value)
            style_metric_cards()
        else:
            final_value = "DOWN"
            st.sidebar.metric(label="OVERALL MOVEMENT", value=final_value)
            style_metric_cards()

if __name__=='__main__':
    main()








