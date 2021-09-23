import plotly.graph_objects as go
import streamlit as st


def format_portfolio(df_portfolio):
    df_portfolio =  df_portfolio.style.format({
        "Weight": "{:.2%}",
        "Target weight": "{:.2%}",
        "Price": "{:,.2f}€",
        "Position": "{:,.2f}€"
    })
    
    return df_portfolio


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
                    It solves the non-linear problem with a non-linear constraint defined as:

                    $$
                    \underset{\Delta s} min \quad \sum_{i} \mid (s_{i} + \Delta s_{i}) \cdot p_{i} - w_{i}^{target} \cdot V \mid + \ C^{\ remaining}
                    \\ \text{s.t} \quad C^{\ remaining} \geq 0
                    $$

                    where 

                    $$
                    \Delta s_{i}: \ \text{number of shares of asset} \ i \ \text{to buy or sell} \\
                    s_{i}: \ \text{number of shares of asset (integer)} \ i \\
                    p_{i}: \ \text{price of asset} \ i \\
                    w_{i}^{target} \ \text{target allocation for asset} \ i \\
                    V = \sum_{i} s_{i} \cdot p_{i} + C: \ \text{total portfolio value} \\
                    C: \ \text{amount of cash to invest} \\
                    C^{\ remaining} = C - \sum_{i} \left( \Delta s_{i} \cdot p_{i} + F(\Delta s_{i}) \right) \ \text{cash remaining after rebalancing} \\
                    F: \ \text{function describing the transaction fees to buy or sell shares} \ \Delta s_{i} \\

                    $$

                    Because the independant variable is discrete, the objective and constraint non-linear (because $F$ is non linear), the optimal solution is searched using scipy implementation of Differential Evolution.
                    """)
