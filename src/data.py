from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from pandas_datareader import data
from pandera import Check, Column, DataFrameSchema, Index, errors


portfolio_schema = DataFrameSchema(
    {
        "Asset": Column(str, allow_duplicates=False),
        "Share": Column(int),
        "Target weight": Column(float, checks=[
            Check(lambda s: (s >= 0.0) & (s <= 1.0)),
            Check(lambda s: np.sum(s) == 1.0)
        ]),
        "Freeze": Column(bool, required=False),
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


def quotes(assets, look_back, end_date=None):
    if end_date:
        start_date = (end_date - timedelta(days=look_back)).strftime("%Y-%m-%d")
    else:
        start_date = (datetime.today() - timedelta(days=look_back)).strftime("%Y-%m-%d")

    df = data.DataReader(assets, "yahoo", start=start_date, end=end_date)
    df = df.stack(level=1).reset_index(level=[0, 1], drop=False).reset_index(drop=True)

    return df
