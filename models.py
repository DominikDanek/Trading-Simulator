import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ticker = "AAPL"
# start_date = "2020-0-01"
# end_date = "2025-07-01"

class Model:
    def __init__(self,s,e,t):
        self.s = s
        self.e = e
        self.t = t
        self.data = yf.download(self.t, start=self.s, end=self.e)

    def plot_returns(self, data):

        plt.figure(figsize=(14, 7))
        plt.plot(data['Cumulative Market Return'], label='Market Return', alpha=0.75)
        plt.plot(data['Cumulative Strategy Return'], label='Strategy Return', alpha=0.75)
        plt.title("Cumulative Returns")
        plt.legend()
        plt.show()

        total_strategy_return = data['Cumulative Strategy Return'].iloc[-1] - 1
        return (total_strategy_return*100).round(2)
    
class moving_average_crossover(Model):
    def get_returns(self, short_window, long_window):
        data = self.data

        data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

        data['Signal'] = 0
        data.loc[data['SMA_short'] > data['SMA_long'], 'Signal'] = 1
        data.loc[data['SMA_short'] < data['SMA_long'], 'Signal'] = -1

        data['Position'] = data['Signal'].shift(1)
        data['Daily Return'] = data['Close'].pct_change()
        data['Strategy Return'] = data['Position'] * data['Daily Return']

        data['Cumulative Market Return'] = (1 + data['Daily Return']).cumprod()
        data['Cumulative Strategy Return'] = (1 + data['Strategy Return']).cumprod()
        return data
class rsi_mean_reversion(Model):
    def get_returns(self,period,overbought,oversold):
        data = self.data

        data["Daily Return"] = data["Close"].pct_change()

        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        data["RSI"] = 100 - (100 / (1 + rs))

        data["Signal"] = 0
        data.loc[data["RSI"] < oversold, "Signal"] = 1
        data.loc[data["RSI"] > overbought, "Signal"] = -1

        # data["Position"] = (data["Signal"].shift(1))

        data["Position"] = (data["Signal"].replace(0, np.nan).ffill().fillna(0).shift(1))

        data["Strategy Return"] = data["Position"] * data["Daily Return"]

        data["Cumulative Market Return"] = (1 + data["Daily Return"]).cumprod()
        data["Cumulative Strategy Return"] = (1 + data["Strategy Return"]).cumprod()

        return data
class logistics_regression(Model):
    def get_returns(self):
        data = self.data

