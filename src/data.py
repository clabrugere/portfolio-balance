import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas_datareader import data


def daily_close(assets, look_back, end_date=None):
    if end_date:
        start_date = (end_date - timedelta(days=look_back)).strftime("%Y-%m-%d")
    else:
        start_date = (datetime.today() - timedelta(days=look_back)).strftime("%Y-%m-%d")

    df = data.DataReader(assets, "yahoo", start=start_date, end=end_date)

    return df["Adj Close"]
