from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st
from pandas_datareader import data
from pandera import Check, Column, DataFrameSchema, Index, errors


portfolio_schema = DataFrameSchema(
    {
        "Assets": Column(str),
        "Shares": Column(int),
        "Weights": Column(float, checks=[
            Check(lambda s: (s >= 0.0) & (s <= 1.0)),
            Check(lambda s: np.sum(s) == 1.0)
        ]),
    },
    index=Index(int),
    strict=True,
    coerce=True,
)


def validate_file(file):
    try:
        df_portfolio = pd.read_csv(file)
        portfolio_schema(df_portfolio)
        return df_portfolio
    
    except errors.SchemaErrors as err:
        raise err


@st.cache(show_spinner=False)
def augment(df_portfolio):
    assets = df_portfolio["Assets"].values.ravel()
    df_prices = quotes(assets, 30)
    
    last_trading_day = df_prices["Date"].max()
    df_portfolio["prices"] = df_prices.loc[df_prices["Date"] == last_trading_day, "Close"].values
    df_portfolio["position"] = df_portfolio["Shares"] * df_portfolio["prices"]
    
    return df_portfolio, df_prices


@st.cache(show_spinner=False)
def quotes(assets, look_back, end_date=None):
    if end_date:
        start_date = (end_date - timedelta(days=look_back)).strftime("%Y-%m-%d")
    else:
        start_date = (datetime.today() - timedelta(days=look_back)).strftime("%Y-%m-%d")

    df = data.DataReader(assets, "yahoo", start=start_date, end=end_date)
    df = df.stack(level=1).reset_index(level=[0, 1], drop=False).reset_index(drop=True)

    return df
