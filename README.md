# 💰Trading-Simulator💰

MODELS.PY

I used three models for this trading simulator

- Moving Average Crossover
- Rsi Mean Reversion
- Logistic Regression

This module is entirely object oriented
4 classes
- its a super class Model
- there are three subclasses for each model
- Model downloads yfinance data as a data frame with Close High Low Open Volume each row is a day
- changes stored in self.data
- plot_returns plots market and strategy returns

Moving Average Crossover

- two averages short and long
- short term change significant then buy or sell
- if long ma surpasses short me then sell
- if short ma surpasses long ma then buy
- signals buy = 1 sell = -1 otherwise 0

Rsi Mean Reversion

- RSI from average losses and gains over a user window
- oversold then buy
- overbought then sell
- zero signals replaced with NaN and other functions

Logistic Regression
- uses machine learning to learn stock movements and outputs probabilities of a stock rising which are used to determine buy/sell signals
- conditions RSI and MA plus Trading Volume and volatility
- uses Sklearn library
- user defines training ratio
- outputs probability of stock rising
- if probability is greater than upper boundry buy
- if probability is lower than the lower boundry sell
- very sensitive parameters, if its not perfect then it often has a -100% return given enough time

All signals are shifted by one to avoid look ahead bias

INTERFACE.PY

This is the Graphical user interface using Tkinter
- acts as the connection between user input and models module
- 
Interface window features listed below:
1. dropdown between RSI Mean Reversion Moving Average Crossover Logistic Regression
2. selected model shows its input fields using seperate frames and combo box
3. User inputs
3. RSI periods
4. moving average windows
5. probability bounds
5. training proportion
6. stock ticker
7. start end dates
8. Run button
9. collects inputs using get
10. initialises model
11. executes selected model
12. plots cumulative market and strategy returns
13. final percentage return displayed at the bottom.

Users can specify indicator parameters such as RSI periods, moving average windows, probability bounds for the logistic regression model, and the proportion of data used for training (only for logistic regression). The interface obviously also includes inputs for the stock ticker and the start/end dates of the simulation.

When the Run button is pressed, the interface collects all user inputs using the get function initialises the model class and then only executes the selected model. It then plots cumulative market returns alongside cumulative strategy returns. The final percentage return of the strategy is displayed at the bottom of the interface.
