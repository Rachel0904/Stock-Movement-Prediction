import traceback
import pandas as pd

def buy_sell(current_row, previous_row):
    try:
        current_william_r = current_row["Williams%R"]
        previous_william_r = previous_row["Williams%R"]

        out_1, out_2 = "NEUTRAL", "HOLD"

        if current_william_r > -20:
            out_1 = "OVERBOUGHT" 
        elif current_william_r < -80:
            out_1 = "OVERSOLD" 
        else:
            out_1 = "NEUTRAL"

        if previous_william_r < -80 and current_william_r > -50:
            out_2 = "BUY" 
            out_3 = "+UPWARD TREND INDICATED"
        elif previous_william_r > -20 and current_william_r < -50:
            out_2 = "SELL"
            out_3 = "-DOWNWARD TREND INDICATED"
        else:
            out_2 = "HOLD"
            out_3 = None

        return out_1, out_2, out_3

    except:
        print(traceback.print_exc())

def get_williams_r(ticker):

    try:
        file_path = "C://Users/Rachel/Desktop/FP/Database/Datasets/" + ticker + '.csv'
        df = pd.read_csv(file_path)
        current_df = df.tail(2)
        return buy_sell(current_df.iloc[-1], current_df.iloc[-2])

    except:
        print(traceback.print_exc())

#print(get_williams_r("AAPL"))