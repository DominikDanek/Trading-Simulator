import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class Model:
    def __init__(self,s,e,t):
        self.s = s
        self.e = e
        self.t = t
        self.data = yf.download(self.t, start=self.s, end=self.e,auto_adjust=False)

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
        data['Daily Return'] = data['Close'].pct_change()

        data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
        data['SMA_change'] = data['SMA_short']- data['SMA_long']

        data['Signal'] = 0
        data.loc[data['SMA_short'] > data['SMA_long'], 'Signal'] = 1
        data.loc[data['SMA_short'] < data['SMA_long'], 'Signal'] = -1

        data['Position'] = data['Signal'].shift(1)
        data['Strategy Return'] = data['Position'] * data['Daily Return']
        data['Cumulative Market Return'] = (1 + data['Daily Return']).cumprod()
        data['Cumulative Strategy Return'] = (1 + data['Strategy Return']).cumprod()
        return data
    
class rsi_mean_reversion(Model):
    def get_money(self,period,overbought,oversold):
        data = self.data

        data["Daily Return"] = data["Close"].pct_change()
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean() #getting the average gain and loss over input period
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss

        data["RSI"] = 100 - (100 / (1 + rs)) #calculate rsi
        data["Signal"] = 0
        data.loc[data["RSI"] < oversold, "Signal"] = 1
        data.loc[data["RSI"] > overbought, "Signal"] = -1

        data["Position"] = (data["Signal"].replace(0, np.nan).ffill().fillna(0).shift(1))
        data["Strategy Return"] = data["Position"] * data["Daily Return"]
        data["Cumulative Market Return"] = (1 + data["Daily Return"]).cumprod()
        data["Cumulative Strategy Return"] = (1 + data["Strategy Return"]).cumprod()

        return data
    
class logistic_regression(Model):
    def __init__(self,s,e,t):
        super().__init__(s,e,t)

        #trained model
        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("lr", LogisticRegression(solver="lbfgs"))])
        
        self.data = yf.download(self.t, start=self.s, end=self.e)[["Close", "Volume"]].dropna()

    def get_features(self,period,short_window,long_window):

        data = self.data.copy()
        data['Daily Return'] = data['Close'].pct_change()
        data['returns'] = data['Daily Return']
        data["volatility"] = data["returns"].rolling(period).std()

        #append moving average diff
        data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
        data['SMA_change'] = data['SMA_short']- data['SMA_long']

        #append rsi
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean() #getting the average gain and loss over input period
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        data["RSI"] = 100 - (100 / (1 + rs))
        data["target"] = (data["Close"].shift(-1) > data["Close"]).astype(int)

        data = data.dropna()
        self.data = data

    def train(self, test_split):
        data = self.data.copy()

        features = [
            "returns",
            "SMA_change",
            "volatility",
            "RSI",
            "Volume",
        ]

        split = int(len(data) * test_split)
        #inputting training data for the sckit library
        X_train = data[features].iloc[:split]
        y_train = data["target"].iloc[:split]
        self.model.fit(X_train, y_train)
        self.features = features
        self.split_index = split
        self.data = data

    def predict_probabilities(self):
        data = self.data
        X = data[self.features]
        probs = self.model.predict_proba(X)[:, 1]
        data["prob_up"] = probs
        return data

    def strategy(self, upper, lower):
        data = self.predict_probabilities()

        data["Signal"] = 0
        data.loc[data["prob_up"] > upper, "Signal"] = 1
        data.loc[data["prob_up"] < lower, "Signal"] = -1

        data["Position"] = data["Signal"].shift(1)
        data["Strategy Return"] = data["Position"] * data["Daily Return"]
        data["Cumulative Market Return"] = (1 + data["Daily Return"]).cumprod()
        data["Cumulative Strategy Return"] = (1 + data["Strategy Return"]).cumprod()
        return data













