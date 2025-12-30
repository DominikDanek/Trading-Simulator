# 💰Trading-Simulator💰
Trading simulator that tests three trading models on any stock between any past date

<<MODELS.PY>>

I used three models for this trading simulator:
- Moving Average Crossover
- Rsi Mean Reversion
- Logistic Regression

This module is entirely object oriented. I have 4 classes, the super class is called 'Model' and it has three subclasses for each model mentioned above. The model class is responsible for downloading the yfinance data for all the models as a data frame that has columns (Close, High, Low, Open, Volume) and each row is a day. Any changes made to the data frame are stored into the attribute self.data. It also has a method 'plot_returns' that plots the market and the strategy returns over the period chosen by the user.

Moving average crossover takes two averages, one for a short time period and one for a longer time period. The idea is that if there is a sudden short term change that is significant enough then the model will buy or sell. If the long term average overcomes the short term average then sell, If the short term average overcomes the long term average then buy. The buys and the shorts are turned into signals so buy = 1 sell = -1, otherwise signal = 0 (when short ma and long ma are equal). 

Rsi Mean reversion uses a relative strength index (RSI) that is caluculated using the average losses and average gains over a window specified by the user. The user then specifies an overbought and oversold level, so If RSI is lower than oversold then buy, and if RSI is greater than overbought level then sell. It can happen that RSI stayes in between these thresholds a lot of the time so I replaced all the zero signals with NaN and other functions to account for that. 

Logistic Regression uses machine learning to learn about a given stock. It learns about its conditions and based on those it observes the resulting day to day change (The conditions in my case were RSI and MA). So for my example it learns if RSI and Moving average difference are x and y amount then the stock increased by z amount. It also takes as input the Trading Volume and its volatility. This is all done internally using the Sklearn library (part of scikit). The user can define what ratio of the time frame they would like to use for training. After learning about its environment it outputs the probability of the stock rising. The user can then specify the boundries for its probability. So if the probability of the stock rising on a given day is higher than the upper boundry then we buy and if its lower than the lower boundry we sell. Unlike the other two that generally have a stable return, logistic regression is very sensitive to its parameters. From my tests if the probability boundries are not perfect, or close to it, then you almost always get a -100% return.

All signals are shifted by one to avoid look ahead bias

<<INTERFACE.PY>>

This module implements a graphical user interface for the trading simulator using Tkinter. Its acts as a connection between the user input and the functionalities of the models module. The interface window contains a dropdown menu that lets the user choose between three models: RSI Mean Reversion, Moving Average Crossover, and Logistic Regression. Based on the selected model, a corresponding set of input fields is displayed. This is done by packing each model into a seperate frames and then using the combo box to display the selected frame.

Users can specify indicator parameters such as RSI periods, moving average windows, probability bounds for the logistic regression model, and the proportion of data used for training (only for logistic regression). The interface also includes inputs for the stock ticker and the start/end dates of the simulation.

When the Run button is pressed, the interface collects all user inputs using the get function initialises the model class and then only executes the selected model. It then plots cumulative market returns alongside cumulative strategy returns. The final percentage return of the strategy is displayed at the bottom of the interface.
