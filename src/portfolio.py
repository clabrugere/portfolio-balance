import numpy as np
from scipy.optimize import NonlinearConstraint, differential_evolution


class Portfolio:
    def __init__(self, shares, cash, fee_func):
        self.shares = shares
        self.cash = cash
        self.fee_func = fee_func
        self.target_weights = None
        self.positions = None
        self.portfolio_value = None
        self.target_positions = None
        self.results = None

    def rebalance(
        self,
        prices,
        target_weights,
        no_selling=True,
        strategy="best1bin",
        init="sobol",
        popsize=30,
        mutation=(0.5, 1.0),
        recombination=0.6,
        seed=None,
    ):

        self.prices = prices
        self.target_weights = target_weights

        self.positions = self.prices * self.shares
        self.portfolio_value = self.positions.sum() + self.cash
        self.target_positions = self.portfolio_value * self.target_weights

        bounds = self._get_bounds(no_selling)
        x0 = np.array([np.mean(b) for b in bounds])
        constraints = NonlinearConstraint(
            self._cash_remaining, 0.0, np.inf, keep_feasible=True
        )

        results = differential_evolution(
            self._objective,
            bounds=bounds,
            strategy=strategy,
            init=init,
            constraints=constraints,
            x0=x0,
            popsize=popsize,
            mutation=mutation,
            recombination=recombination,
            seed=seed,
        )
        self.results = results

        return results.success, np.round(results.x).astype(int)

    def _get_bounds(self, no_selling):
        max_share_delta = np.abs(self.target_positions - self.positions) / self.prices
        hb = np.ceil(max_share_delta) + 1.0

        if no_selling:
            lb = np.zeros(len(hb))
        else:
            lb = -hb

        return list(zip(lb, hb))

    def _cash_remaining(self, shares_delta):
        shares_delta = np.round(shares_delta)
        position_delta = shares_delta * self.prices
        fees = np.array([self.fee_func(x) for x in position_delta])

        return self.cash - (position_delta.sum() + fees.sum())

    def _objective(self, shares_delta):
        cash_remaining = self._cash_remaining(shares_delta)
        position_delta = np.abs(
            self.positions
            + np.round(shares_delta) * self.prices
            - self.target_positions
        ).sum()

        return position_delta + cash_remaining


def fees_func(x):
    x = np.abs(x)

    if x == 0:
        return 0.0
    elif x < 1000:
        return 2.5
    elif 1000 <= x < 5000:
        return 5.0
    elif 5000 <= x < 7500:
        return 7.5
    elif 7500 <= x < 10000:
        return 10.0
    else:
        return 0.001 * x
