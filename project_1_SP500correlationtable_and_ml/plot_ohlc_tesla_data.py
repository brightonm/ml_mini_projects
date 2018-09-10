#!/usr/bin/env python3
"""
Plot OHLC Tesla financial data
"""

import datetime as dt # Set starting and ending times of data we want to pull
import matplotlib.pyplot as plt
from matplotlib import style # In order to have good looking graphs
from mpl_finance import candlestick_ohlc # candlestick used in finance
import matplotlib.dates as mdates
import pandas as pd # Data analysis library
pd.core.common.is_list_like = pd.api.types.is_list_like # Correct a recent bug
import pandas_datareader.data as web # Grab data from the Yahoo Finance API, returns panda dataframe

def main():
    """
    Principal function
    """
    style.use('ggplot') # Setting up a style
    '''
    Getting data from Yahoo Finance API
    '''
    # start = dt.datetime(2005, 1, 1) # Setting up a starting date 1/01/2005
    # end = dt.datetime(2018, 6, 21) # Setting up an ending data 21/06/2018
    #
    # df = web.DataReader('TSLA', 'yahoo', start, end) # Dataframe from Tesla stock from Yahoo API
    # print(df.head(10), '\n') # Print the first ten rows of our dataset
    # print(df.tail(10)) # Print the last ten rows of our dataset
    # df.to_csv('tsla.csv') # Creating a csv file with all the data

    '''
    Getting data from a csv file and good looking printing
    '''
    df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

    '''
    Graphs
    '''
    # df['Adj Close'].plot()
    # plt.show()

    '''
    Stock data manipulation
    '''
    # df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()# Add a new column 100 moving average
    # df.dropna(inplace=True)
    # print(df.tail())
    # ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    # ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    # ax1.plot(df.index, df['Adj Close'])
    # ax1.plot(df.index, df['100ma'])
    # ax2.bar(df.index, df['Volume'])

    '''
    Resample data (e.g one day to ten days)
    '''
    df_ohlc = df['Adj Close'].resample('10D').ohlc() # Creating a new dataframe open high low close
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num) # Conversion dates in matplotlib dates for using candles

    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)


    plt.show()



main()
