# -*- coding: utf-8 -*-
"""
STRATEGY ONE
DESCRIPTION:
    THe main idea of this strategy is to build upon my current strategy. I noticed
    over investing using the magic formula that some prices continue to fall after I invest
    and it would be more ideal if I could invest in them before they rise and sell before they
    fall. for this stragegy I will use the "magic formula" to screen stocks and then
    using boilinger bands and macd to determine when to actually buy/sell the magic
    formula stocks
EXECUTION:
    1.) grab all of the magic formula stocks from "https://www.magicformulainvesting.com/"
    2.) grab the chart information for this data from yahoo finance
    3.) run the techincal indictors on the chart information
    4.) have the program buy or sell
"""
# -*- coding: utf-8 -*-
from webScraper import getMagicFormulaStocks

#STEP ONE
path = ""
email = ""
password = ""
tickers = []
getMagicFormulaStocks(path, email, password, tickers)

# Import necesary libraries
import yfinance as yf
import numpy as np

# Download historical data for required stocks
ohlcv_data = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='6mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp

def Boll_Band(DF, n=14):
    "function to calculate Bollinger Band"
    df = DF.copy()
    df["MB"] = df["Adj Close"].rolling(n).mean()
    df["UB"] = df["MB"] + 2*df["Adj Close"].rolling(n).std(ddof=0)
    df["LB"] = df["MB"] - 2*df["Adj Close"].rolling(n).std(ddof=0)
    df["BB_Width"] = df["UB"] - df["LB"]
    return df[["MB","UB","LB","BB_Width"]]

def RSI(DF, n=14):
    "function to calculate RSI"
    df = DF.copy()
    df["change"] = df["Adj Close"] - df["Adj Close"].shift(1)
    df["gain"] = np.where(df["change"]>=0, df["change"], 0)
    df["loss"] = np.where(df["change"]<0, -1*df["change"], 0)
    df["avgGain"] = df["gain"].ewm(alpha=1/n, min_periods=n).mean()
    df["avgLoss"] = df["loss"].ewm(alpha=1/n, min_periods=n).mean()
    df["rs"] = df["avgGain"]/df["avgLoss"]
    df["rsi"] = 100 - (100/ (1 + df["rs"]))
    return df["rsi"]

# looping over tickers and storing Boll_Band and RSI
for ticker in ohlcv_data:
    ohlcv_data[ticker][["MB","UB","LB","BB_Width"]] = Boll_Band(ohlcv_data[ticker], 30)
    ohlcv_data[ticker]["RSI"] = RSI(ohlcv_data[ticker], 13)

#quick scan to see if any of the undervalued stocks are bellow there mid band,
#if so then buy
for ticker in ohlcv_data:
    if ohlcv_data[ticker]["Adj Close"][125] < ohlcv_data[ticker]["MB"][125]:
        print(ticker)







