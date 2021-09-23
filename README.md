# Portfolio balance

Streamlit application to rebalance a security portfolio automatically based on a target allocation and current market prices.

## Installation

Clone the repository by running the command:

`
git clone https://github.com/clabrugere/portfolio-balance.git
`

In a new environment, install the required packages:

`
pip install -r requirements.txt
`

## Usage

Upload a csv file with the following columns: 
* Asset: tickers (yahoo style "\<stock>.\<exchange>", e.g. "CW8.PA") of your current/desired positions
* Share: number of shares currently owned (0 for asset you would like to include in the portfolio)
* Weight: target allocation. The column must sum to 1

_Note that the security needs to be available in yahoo finance._

Select the amount of cash you want to invest, and click "Balance"

## How it works

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

## License

[MIT](LICENSE)