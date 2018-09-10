#!/usr/bin/env python3
"""
Getting all the data of all the S&P500 stocks and making a correlation table
"""

import bs4 as bs # beautiful soup : web script
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os # In order to create new directories for us
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like # Correct a recent bug
import pandas_datareader.data as web
import pickle # Save any object like variable
import requests # Web requests

style.use('ggplot')

def save_sp500_tickers():
    """
    Automating the saving of S&P500 tickers (that change over time) by parsing wikipedia
    """
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies') # Getting HTML source code of the page
    soup = bs.BeautifulSoup(resp.text, 'lxml') # BeautifulSoup object (specify a parser : lxml)
    table = soup.find('table', {'class' : 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]: # tr = table row
        ticker = row.findAll('td')[0].text # td: table data, each colomn basically, 0 : tickers
        mapping = str.maketrans('.', '-') # Yahoo understand BRK-B and not BRK.B
        ticker = ticker.translate(mapping)
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f) # Dumping tickers in the file f

    # print(tickers) # for debugging

    return tickers

# save_sp500_tickers()

def avoid_errors(ticker, start, end):
    '''
    Automating the relaunch of data pulling if Yahoo crash
    '''
    try:
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv('stocks_dfs/{}.csv'.format(ticker))
    except:
        avoid_errors(ticker, start, end)


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers() # uptdating the tickers if asked
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    """
    Getting all the stock data and convert all of them in their own csv file
    and store them in their directory because it takes some time to pull them
    from Yahoo
    """
    if not os.path.exists('stocks_dfs'): # Create a directory if it does not exist
        os.makedirs('stocks_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime(2018, 6, 21)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stocks_dfs/{}.csv'.format(ticker)):
            avoid_errors(ticker, start, end)
        else:
            print('Already have {}'.format(ticker))


# get_data_from_yahoo()

def compile_data():
    """
    Compiling all the adjusted close prices in one dataframe
    """
    with open ("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv("stocks_dfs/{}.csv".format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns = {'Adj Close':ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer') # We don't loose data in the numbers of rows or columns is not matching

        if count % 10 == 0: # Knowing where we are
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

# compile_data()

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    # df['AAPL'].plot()
    # plt.show()
    df_corr = df.corr() # Create a correlation table out of our dataframe

    print(df_corr.head())

    data = df_corr.values # numpy array of the columns and rows but only the values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1) # one by one and plot number one

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn) # allow us to plot some colors grid, cmap : range
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False) # setting our ticks
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis() # avoid spaces on y axis
    ax.xaxis.tick_top() # put the xaxis on top cause here look more like a table

    column_labels = df_corr.columns
    row_labels = df_corr.index # those shoud be identical, same size

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90) #rotation of the xticks
    heatmap.set_clim(-1,1) # minimum and maximum
    plt.tight_layout() # clean everything up cause it should be a messy graph
    plt.show()


visualize_data()
