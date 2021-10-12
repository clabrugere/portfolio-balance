import logging

import numpy as np
import streamlit as st

from src import data, visualization
from src.portfolio import Portfolio, fees_func

logging.basicConfig(level=logging.INFO)


@st.cache(show_spinner=False)
def fetch_quotes(df_portfolio):
    assets = df_portfolio["Asset"].values.ravel()
    df = data.prices(assets, 0)

    return df


def load_portfolio(file, cash):
    df_portfolio = data.validate_file(file)
    df_prices = fetch_quotes(df_portfolio)

    last_trading_day = df_prices["Date"].max()
    prices = df_prices.loc[df_prices["Date"] == last_trading_day, "Close"].values

    if "Target Price" in df_portfolio.columns:
        target_prices = df_portfolio["Target Price"].values
        prices[~np.isnan(target_prices)] = target_prices[~np.isnan(target_prices)]
        df_portfolio = df_portfolio.drop("Target Price", axis=1)

    df_portfolio["Price"] = prices
    df_portfolio["Position"] = df_portfolio["Share"] * df_portfolio["Price"]
    df_portfolio["Weight"] = df_portfolio["Position"] / (df_portfolio["Position"].sum() + cash)

    logging.info(f"shape of loaded portfolio: {df_portfolio.shape}")

    return df_portfolio


def balance(df_portfolio, cash, no_selling):
    shares = df_portfolio["Share"].values.ravel()
    prices = df_portfolio["Price"].values.ravel()
    target_weights = df_portfolio["Target weight"].values.ravel()

    portfolio = Portfolio(shares, cash, fees_func)
    success, shares_delta = portfolio.balance(prices, target_weights, no_selling=no_selling)

    if success:
        logging.info(f"sucessful optimization. Solution: {shares_delta}")
    else:
        logging.warning(f"the optimization did not converge. Solution: {shares_delta}")

    transactions = shares_delta * prices
    fees = np.array([fees_func(t) for t in transactions])
    cash_leftover = cash - (transactions.sum() + fees.sum())

    df_portfolio_balanced = df_portfolio.copy()
    df_portfolio_balanced["Share"] = df_portfolio_balanced["Share"] + shares_delta
    df_portfolio_balanced["Buy/sold"] = shares_delta
    df_portfolio_balanced["Position"] = df_portfolio_balanced["Share"] * df_portfolio_balanced["Price"]
    df_portfolio_balanced["Weight"] = df_portfolio_balanced["Position"] / (
                df_portfolio_balanced["Position"].sum() + cash_leftover)

    return df_portfolio_balanced, transactions, fees, cash_leftover, success


st.set_page_config(
    page_title="Portfolio balancer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
)

with st.sidebar:
    st.title("Portfolio balancing")
    st.caption("Optimize the balancing of your portfolio.")

    with st.form("portfolio_settings"):
        st.markdown(
            r"""
            Upload a csv file with the following columns: 
            * Asset: tickers (yahoo style) of your current/desired positions
            * Share: number of shares currently owned (0 for asset you would like to include in the portfolio)
            * Target weight: target allocation. The column must sum to 1
            """
        )
        file = st.file_uploader("", "csv")
        cash = st.number_input("Cash available", min_value=0., value=1000.0)
        no_selling = st.checkbox("No sell operation", value=True)
        submitted = st.form_submit_button("Balance")

        if file is not None:
            df_portfolio = load_portfolio(file, cash)

if file is not None and submitted and (cash > 0.0 or no_selling is False):

    with st.spinner("Just a second..."):
        df_portfolio_balanced, transactions, fees, cash_remaining, success = balance(df_portfolio, cash, no_selling)

    if success:
        st.success("Optimization successfull!")
    else:
        st.error("No solution was found!")

    visualization.how_it_works()
    col_current, col_rebalanced = st.columns(2)

    with col_current:
        df_portfolio = df_portfolio[["Asset", "Share", "Weight", "Target weight", "Price", "Position"]]
        visualization.summary(df_portfolio, cash, "Current")

    with col_rebalanced:
        df_portfolio_balanced = df_portfolio_balanced[
            ["Asset", "Share", "Weight", "Target weight", "Price", "Position", "Buy/sold"]]
        visualization.summary(df_portfolio_balanced, cash_remaining, "Rebalanced")
        st.text(f"Fees: {fees.sum():,.2f}€")
