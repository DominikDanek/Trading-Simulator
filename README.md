# Trading-Simulator
Trading simulator that tests three trading models on any stock between any past date

<<MODELS.PY>>
I used three models for this trading simulator:
- Moving Average Crossover
- Rsi Mean Reversion
- Logistic Regression

This module is entirely object oriented. I have 4 classes, the super class is called 'Model' and it has three subclasses for each model mentioned above. The model class is responsible for downloading the yfinance data for all the models. It also has a method 'plot_returns' that plots the market and the strategy returns over the period chosen by the user
Mving average crossover take two averages, one for a short time period and one for a longer time period. The idea is that if there is a sudden short term change that is significant enough then the model will buy or sell. If the long term average is lower than the short term average then 
