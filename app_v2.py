import numpy as np
import pandas as pd
import streamlit as st

from src import ui, data
from src.portfolio import Portfolio, fees_func


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
        file = st.file_uploader("Upload portfolio", "csv")
        
        if file is not None:
            df_portfolio = data.validate_file(file)
            df_portfolio, df_prices = data.augment(df_portfolio)            
        
        cash = st.number_input("Cash available", min_value=0., value=1000.0)
        submitted = st.form_submit_button("Balance")
        

if submitted and cash > 0.0:
    
    col_current, col_rebalanced = st.columns(2)
    with col_current:
        ui.summary(df_portfolio, "Current")
    
    with col_rebalanced:
        ui.summary(df_portfolio, "Rebalanced")