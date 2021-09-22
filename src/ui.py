import streamlit as st
import pandas as pd
import plotly.graph_objects as go


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


def summary(df_portfolio, label):
    st.header(label)
    
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=df_portfolio["Assets"],
            values=df_portfolio["Weights"]
        )
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig)
    st.dataframe(df_portfolio)
    st.subheader("Total positions: €")


def operations(df_operations):
    pass