import os
import pandas as pd
import yfinance as yf
import datetime as dt

try:
    from Features import create_features
except:
    from Database.Features import create_features

import traceback

class DATABASE:

    def __init__(self):
        pass

    def update_data(self, ticker):
        try:
            ticker_ = yf.Ticker(ticker)
            df = ticker_.history(period="10y")

            # Creating Features and Target variable
            df = create_features(df)

            file_path = "C://Users/Rachel/Desktop/FP/Database/Datasets/" + ticker + '.csv'
            df.to_csv(file_path)

            return 1

        except:
            print("Error in creating Initial Data for {}".format(ticker))
            print(traceback.print_exc())
            return 0

    def get_current_day_data(self, ticker):
        try:
            update_status = self.update_data(ticker)

            if update_status == 1:
                file_path = "C://Users/Rachel/Desktop/FP/Database/Datasets/" + ticker + '.csv'
                df = pd.read_csv(file_path)
                current_df = df.tail(1)
                return current_df

        except:
            print("Error in getting current day data for {}".format(ticker))
            print(traceback.print_exc())
            return -2

"""
database = DATABASE()
#update_status = database.update_data("AAPL")
#print("update_status: ", update_status)
current_day_data = database.get_current_day_data("AAPL")
# Checking if Scaled Data working
import pickle
import joblib
ct1 = joblib.load("C://Users/Rachel/Desktop/FP/Model/Scaler/AAPL")
technical_indicators = ["volume", "SMA_10", "SMA_20", "SMA_50", "SMA_100", "SMA_200", "EMA_10", "EMA_20", "EMA_50", "EMA_100", "EMA_200", "ATR", "ADX", "CCI", "ROC", "RSI", "Williams%R", "SO%K"]
current_day_data = current_day_data[technical_indicators].copy()
scaled_processed = ct1.transform(current_day_data)
print("scaled_processed: ",scaled_processed)
model_file_path = "C://Users/Rachel/Desktop/FP/Model/Model_Pickle/" + "AAPL" + '.pkl'
model = pickle.load(open(model_file_path, 'rb'))
prediction = model.predict(scaled_processed)
print("prediction: ", prediction)
"""