import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def format_portfolio(df_portfolio):
    df_portfolio =  df_portfolio.style.format({
        "Weight": "{:.2%}",
        "Target weight": "{:.2%}",
        "Price": "{:,.2f}€",
        "Position": "{:,.2f}€"
    })
    
    return df_portfolio


def assets_value(df_prices):
    st.header("Assets value")
    
    fig = go.Figure()
    for a in df_prices["Symbols"].unique():
        df_asset = df_prices[df_prices["Symbols"] == a]
        fig.add_trace(
            go.Candlestick(
                name=a,
                x=df_asset["Date"],
                open=df_asset["Open"],
                close=df_asset["Close"],
                high=df_asset["High"],
                low=df_asset["Low"]
            )
        )
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig)


def summary(df_portfolio, cash, label):
    st.header(label)
    
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=list(df_portfolio["Asset"]) + ["Cash"],
            values=list(df_portfolio["Position"]) + [cash],
            sort=False
        )
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig)
    st.dataframe(format_portfolio(df_portfolio))
    st.subheader(f"Total positions: {df_portfolio['Position'].sum():,.2f}€")
    st.subheader(f"Cash: {cash:,.2f}€")


def how_it_works():
    with st.expander("How it works"):
        st.markdown(r"""
                    It solves a non-linear problem with a non-linear constraint defined as:
                    
                    $$
                    \underset{\Delta s} min \quad \sum_{i} \mid ( s_{i} + \Delta s_{i} - s_{i}^{target} ) \cdot p_{i} \mid + \ C - \sum_{i} ( \Delta s_{i} \cdot p_{i} + F(\Delta s_{i}) )
                    \\ \text{s.t} \quad 0 \leq \sum_{i} \Delta s_{i} + F(\Delta s_{i}) \leq C
                    $$
                    
                    where 
                    
                    $$
                    s_{i}: \ \text{number of shares of asset (integer)} \ i \\
                    s_{i}^{target}: \ \text{number of shares of asset} \ i \ \text{to satisfy the target allocation} \\
                    \Delta s_{i}: \ \text{number of shares of asset} \ i \ \text{to buy or sell} \\
                    p_{i}: \ \text{price of asset} \ i \\
                    F: \ \text{function describing the transaction fees to buy or sell shares} \ \Delta s_{i} \\
                    C: \ \text{amount of cash to invest} \\
                        
                    \ C - \sum_{i} ( \Delta s_{i} \cdot p_{i} + F(\Delta s_{i}) ) \ \text{is then the leftover cash after rebalancing}
                    
                    $$
                    
                    Because the independant variable is discrete, the objective and constraint non-linear (because $F$ is non linear), the optimal solution is searched using scipy implementation of Differential Evolution.
                    """)
