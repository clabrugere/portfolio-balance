import numpy as np
import pandas as pd
import streamlit as st

from src import data
from src.portfolio import Portfolio, fees_func


@st.cache(show_spinner=False)
def get_last_prices(assets):
    return data.daily_close(assets, 0).values.ravel()


def get_metrics(prices, shares, cash, target_weights, share_buy):
    positions = prices * shares
    portfolio_value = positions.sum() + cash
    
    transaction = shares_buy * prices
    fees = np.array([fees_func(x) for x in shares_buy * prices])
    cash_leftover = cash - (transaction.sum() + fees.sum())
    
    positions_new = (shares + shares_buy) * prices
    weights_new = positions_new / portfolio_value
    
    return transaction, fees, cash_leftover, weights_new


st.set_page_config(
    page_title="Portfolio balancer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
)
st.title("Porfolio balancer")

df_portfolio = pd.DataFrame({
    "assets": ["CW8.PA", "PAEEM.PA", "RS2K.PA", "SMC.PA", "EESM.PA"],
    "shares": [53, 51, 4, 1, 2],
    "target_weights": [.84, .04, .06, .03, .03]
})

st.header("Settings")
with st.form("portfolio_settings"):
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(df_portfolio.style.format({"target_weights": "{:.2%}"}))
    
    with col2:
        cash = st.number_input("Cash available", min_value=1000.0)
        no_selling = st.checkbox("No sell operation", value=True)
    
    submitted = st.form_submit_button("Balance")

if submitted and cash > 0.0:
    assets = df_portfolio["assets"].values.ravel()
    shares = df_portfolio["shares"].values.ravel()
    target_weights = df_portfolio["target_weights"].values.ravel()
    
    portfolio = Portfolio(shares, cash, fees_func)
    
    with st.spinner("Rebalancing..."):
        prices = get_last_prices(assets)
        shares_buy = portfolio.rebalance(prices, target_weights, no_selling=no_selling)
        
        transaction, fees, cash_leftover, weights_new = get_metrics(prices, shares, cash, target_weights, shares_buy)
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.header("Operations")
        for a, s, p, f in zip(assets, shares_buy, prices, fees):
            if s != 0.:
                op_type = "buy" if s > 0. else "sell"
                s = int(s)
                cash_delta = -1 * s * p
                
                st.text(f"{a}: {op_type} {np.abs(s)} @ {p:.2f}€ ({-1 * s * p:.2f}€ -{f:.2f}€)")
        
        st.header("Resulting allocation")
        df_new_allocation = pd.DataFrame({
            "assets": assets,
            "shares": (shares + shares_buy).astype(int),
            "weights": weights_new
        })
        st.dataframe(df_new_allocation.style.format({"weights": "{:.2%}"}))
        
    
    with col2:
        st.header("Cash balance")
        
        st.caption("Cash invested")
        st.text(f"{transaction.sum():.2f}€")

        st.caption("Fees")
        st.text(f"{fees.sum():.2f}€")
        
        st.caption("Cash leftover")
        st.text(f"{cash_leftover:.2f}€")
