import numpy as np
import pandas as pd
import streamlit as st

from src import ui, data
from src.portfolio import Portfolio, fees_func


def rebalance(df_portfolio, cash, no_selling):
    shares = df_portfolio["Share"].values.ravel()
    prices = df_portfolio["Price"].values.ravel()
    target_weights = df_portfolio["Target weight"].values.ravel()
    
    portfolio = Portfolio(shares, cash, fees_func)
    shares_buy = portfolio.rebalance(prices, target_weights, no_selling=no_selling)
    transactions = shares_buy * prices
    fees = np.array([fees_func(x) for x in transactions])
    cash_leftover = cash - (transactions.sum() + fees.sum())
    
    df_portfolio_balanced = df_portfolio.copy()
    df_portfolio_balanced["Share"] = df_portfolio_balanced["Share"] + shares_buy.astype(int)
    df_portfolio_balanced["Buy/sold"] = shares_buy.astype(int)
    df_portfolio_balanced["Position"] = df_portfolio_balanced["Share"] * df_portfolio_balanced["Price"]
    df_portfolio_balanced["Weight"] = df_portfolio_balanced["Position"] / (df_portfolio_balanced["Position"].sum() + cash_leftover)
    
    return df_portfolio_balanced, transactions, fees, cash_leftover


st.set_page_config(
    page_title="Portfolio balancer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
)

with st.sidebar:
    st.title("Portfolio balancing")
    st.caption("Optimize the rebalancing of your portfolio.")
    
    with st.form("portfolio_settings"):
        
        st.markdown("""
                    Upload a csv file with the following columns: 
                    * Asset: tickers (yahoo style) of your current/desired positions
                    * Share: number of shares currently owned (0 for asset you would like to include in the portfolio)
                    * Weight: target allocation. The column must sum to 1
                    """)
        file = st.file_uploader("", "csv")
        cash = st.number_input("Cash available", min_value=0., value=1000.0)
        no_selling = st.checkbox("No sell operation", value=True)
        
        if file is not None:
            df_portfolio = data.validate_file(file)
            df_portfolio, df_prices = data.augment(df_portfolio, cash)    
        
        submitted = st.form_submit_button("Balance")
        

if submitted and cash > 0.0:
    
    with st.spinner("Just a second..."):
        df_portfolio_rebalanced, transactions, fees, cash_leftover = rebalance(df_portfolio, cash, no_selling)
    
    col_current, col_rebalanced = st.columns(2)
    with col_current:
        df_portfolio = df_portfolio[["Asset", "Share", "Weight", "Target weight", "Price", "Position"]]
        ui.summary(df_portfolio, cash, "Current")
    
    with col_rebalanced:
        df_portfolio_rebalanced = df_portfolio_rebalanced[["Asset", "Share", "Weight", "Target weight", "Price", "Position", "Buy/sold"]]
        ui.summary(df_portfolio_rebalanced, cash_leftover, "Rebalanced")
        st.subheader(f"Fees: {fees.sum():,.2f}€")
