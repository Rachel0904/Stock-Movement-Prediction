# Import Libraries
import pandas as pd
import numpy as np
import traceback

# Technical Indicators
def get_adx(high, low, close, lookback):
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.rolling(lookback).mean()

    plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha = 1/lookback).mean()
    return plus_di, minus_di, adx_smooth

# Function to calculate Relative Strength Index (RSI)
def compute_rsi(close_prices, window=14):
    price_diff = close_prices.diff(1)
    gain = price_diff.where(price_diff > 0, 0)
    loss = -price_diff.where(price_diff < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_wr(high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = -100 * ((highh - close) / (highh - lowl))
    return wr

def create_features(df):
    print("Entering create_features")

    try:
        df.columns = ['open', 'high', 'low', 'close', 'volume', 'Dividends', 'Stock Splits']

        ti = pd.DataFrame(index=df.index)
        ti.index.name = "date"

        # open, high, low, close, volume
        ti["open"] = df["open"]
        ti["high"] = df["high"]
        ti["low"] = df["low"]
        ti["close"] = df["close"]
        ti["volume"] = df["volume"]

        # Simple Moving Average
        ti["SMA_10"] = (sum(ti.close, 10))/10
        ti["SMA_20"] = (sum(ti.close, 20))/20
        ti["SMA_50"] = (sum(ti.close, 50))/50
        ti["SMA_100"] = (sum(ti.close, 100))/100
        ti["SMA_200"] = (sum(ti.close, 200))/200

        # Exponential Moving Average
        ti["EMA_10"] = ti.close.ewm(span=10).mean().fillna(0)
        ti["EMA_20"] = ti.close.ewm(span=20).mean().fillna(0)
        ti["EMA_50"] = ti.close.ewm(span=50).mean().fillna(0)
        ti["EMA_100"] = ti.close.ewm(span=100).mean().fillna(0)
        ti["EMA_200"] = ti.close.ewm(span=200).mean().fillna(0)

        # Average True Range
        # Calculate True Range (TR)
        ti['High-Low'] = ti['high'] - ti['low']
        ti['High-PrevClose'] = abs(ti['high'] - ti['close'].shift(1))
        ti['Low-PrevClose'] = abs(ti['low'] - ti['close'].shift(1))
        ti['TR'] = ti[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

        # Calculate Average True Range (ATR)
        period = 14  # ATR period
        ti['ATR'] = ti['TR'].rolling(period).mean()

        # Average Directional Index
        ti["ADX"] = pd.DataFrame(get_adx(ti['high'], ti['low'], ti['close'], 14)[2]).rename(columns = {0:'ADX'})

        # Commodity Channel Index
        #ti["CCI"] = talib.CCI(ti.high, ti.low, ti.close, timeperiod=20)
        tp = (ti["high"] + ti["low"] + ti["close"]) / 3
        ma = tp / 20
        md = (tp - ma) / 20
        ti["CCI"] = (tp - ma)/(0.015*md)

        # Price rate-of-change
        #ti["ROC"] = talib.ROC(ti.close)
        ti["ROC"] = ((ti["close"] - ti["close"].shift(12))/(ti["close"].shift(12)))*100

        # Relative Strength Index
        ti["RSI"] = compute_rsi(ti["close"])

        # William’s %R
        ti["Williams%R"] = get_wr(ti['high'], ti['low'], ti['close'], 14)

        # Stochastic %K
        ti["SO%K"] = (ti.close - ti.low)/(ti.high - ti.low)

        # Create Target Variable
        ti["Target"] = np.where(ti.close.shift(-1) > ti.close, 1, 0)

        return ti

    except:
        print(traceback.print_exc())
