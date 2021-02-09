from pandas_datareader import data
import numpy as np
import pandas as pd
import datetime as dt


def closePrices(tickers_list):
    """Returns a DataFrame of two columns containing the daily prices of both tickers. \n\n tickers_list: a list with two stock tickers.
    If ticker not supported by Yahoo API, a ValueError will be raised \n"""

    # list for appending each pandas Series, for each ticker on list
    series_list = []

    END_DATE = str(dt.date.today())  # today date

    START_DATE = str(dt.date.today() - dt.timedelta(days=16000))  # remote enough date

    for ticker in tickers_list:

        try:

            closePrices = data.DataReader(ticker, 'yahoo', start=START_DATE, end=END_DATE)['Close']  # obtaining prices

            series_list.append(closePrices)

        except:

            raise ValueError('Invalid ticker: "{}"'.format(ticker))  # error will raise if ticker is not valid

            break

    # getting common indexes (days) for both stocks:

    common_indexes = np.intersect1d(series_list[0].index, series_list[1].index)

    # concatenating both Series objects for the final DataFrame

    closePricesdf = pd.concat([series_list[0].loc[common_indexes],
                               series_list[1].loc[common_indexes]], axis=1)

    # naming columns correctly

    closePricesdf.columns = [tickers_list[0], tickers_list[1]]

    # finally, obtaining the DataFrame

    return closePricesdf
