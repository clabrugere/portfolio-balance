# Portfolio balance

![Portfolio balancer](static/portfolio_balancer.png "Portfolio balancer")

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

## License

[MIT](LICENSE)