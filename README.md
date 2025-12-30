# Trading-Simulator
Trading simulator that tests three trading models on any stock between any past date

<<MODELS.PY>>

I used three models for this trading simulator:
- Moving Average Crossover
- Rsi Mean Reversion
- Logistic Regression

This module is entirely object oriented. I have 4 classes, the super class is called 'Model' and it has three subclasses for each model mentioned above. The model class is responsible for downloading the yfinance data for all the models as a data frame that has columns (Close, High, Low, Open, Volume) and each row is a day. Any changes made to the data frame are stored into the attribute self data. It also has a method 'plot_returns' that plots the market and the strategy returns over the period chosen by the user.

Moving average crossover takes two averages, one for a short time period and one for a longer time period. The idea is that if there is a sudden short term change that is significant enough then the model will buy or sell. If the long term average overcomes the short term average then sell, If the short term average overcomes the long term average then buy. The buys and the shorts are turned into signals so buy = 1 sell = -1, otherwise signal = 0 (when short ma and long ma are equal). 

Rsi Mean reversion uses a relative strength index (RSI) that is caluculated using the average losses and average gains over a window specified by the user. The user then specifies an overbought and oversold level, so If RSI is lower than oversold then buy, and if RSI is greater than overbought level then sell. It can happen that RSI stayes in between these thresholds a lot of the time so I replaced all the zero signals with NaN and other functions to account for that. 

Logistic Regression uses machine learning to learn about a given stock. It learns about its conditions and based on that it observes the resulting day to day change. The conditions for my example were RSI and MA. So for my example it learns if RSI and Moving average difference are x and y amount then the stock increased by z amount. It also takes as input the Traing Volume and its volatility. This is all done internally using the Sklearn library (part of scikit). The user can define what ratio of the time frame they would like to use for training. After learning about its environment it outputs the probability of the stock rising. The user can then specify the boundries for its probability. So if the probability of the stock rising on a given day is higher than the upper boundry then we buy and if its lower than the lower boundry we sell.

All signals are shifted by one to avoid look ahead bias
