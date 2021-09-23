import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def format_portfolio(df_portfolio):
    df_portfolio =  df_portfolio.style.format({
        "Weights": "{:.2%}",
        "Target weights": "{:.2%}",
        "Prices": "{:,.2f}€",
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
            labels=list(df_portfolio["Assets"]) + ["Cash"],
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
