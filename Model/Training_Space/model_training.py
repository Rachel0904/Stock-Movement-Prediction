# Importing Required Libraries
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from Config.top_25_tickers import tickers_dict
from Config.technical_indicators import technical_indicators
from Database.functions import DATABASE

database = DATABASE()

tickers_dict = tickers_dict
tickers_list = list(tickers_dict.keys())

class TRAIN:

    def __init__(self, ticker):
        self.ticker = ticker

    def train_test_split(self, stock_df, test_size):
        # Separating Features and the Target
        stock_x = stock_df.drop(columns=["Target"])
        stock_y = stock_df["Target"]

        slice_ = int(len(stock_df) * test_size)

        # Train Data
        stock_x_train = stock_x.iloc[0:slice_]
        stock_y_train = stock_y.iloc[0:slice_]

        # Test Data
        stock_x_test = stock_x.iloc[slice_:]
        stock_y_test = stock_y.iloc[slice_:]

        return stock_x_train, stock_y_train, stock_x_test, stock_y_test
    
    def scaling_pipeline(self, stock_df):
        stock_x = stock_df.drop(columns=["Target"])

        # Define scaling pipeline
        scale_pipeline = Pipeline([('scale', MinMaxScaler())])
        scale_preprocess_pipeline = ColumnTransformer([('scale', scale_pipeline, stock_x.columns)]) 
        scale_processed = scale_preprocess_pipeline.fit(stock_x)

        file_path = "C://Users/Rachel/Desktop/FP/Model/Scaler/" + self.ticker 
        joblib.dump(scale_processed, file_path)

        return scale_processed

for ticker in tickers_list[0:1]:
    update_response = database.update_data(ticker)
    if update_response == -2:
        print("Error in Updating the Database.")

    file_path = "C://Users/Rachel/Desktop/FP/Database/Datasets/" + ticker + '.csv'
    df = pd.read_csv(file_path)

    df = df.dropna()
    df = df[~df.isin([df.nan, df.inf, -df.inf]).any(axis=1)]

    df = df[technical_indicators + ['Target']]

    training = TRAIN(ticker=ticker)
    scale_processed = training.scaling_pipeline(df)
    stock_x_train, stock_y_train, stock_x_test, stock_y_test = training.train_test_split(df, test_size=0.05)
    
    stock_x_train_scaled = scale_processed.transform(stock_x_train)
    stock_x_test_scaled = scale_processed.transform(stock_x_test)

    #training.export_tpot(stock_x_train_scaled, stock_y_train)

