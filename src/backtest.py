import pandas as pd
import numpy as np
import matplotlib as plt

from strategy import run_strategy, monthly_returns

def run_backtest(signals, weights, N):
    changes = (signals - signals.shift(1)).abs().sum(axis=1)
    changes.iloc[0] = 2*N
    buys = changes / 2
    turnover = buys / N
    rate = 0.005        
    transaction_costs = turnover * rate
    
    #PORTFOLIO RETURNS ACROSS ALL DATES
    portfolio_returns_matrix = (weights.shift(1) * monthly_returns)
    portfolio_returns = portfolio_returns_matrix.sum(axis=1, min_count=1)
    net_portfolio_returns = portfolio_returns - transaction_costs.shift(1)
    return net_portfolio_returns

#TEST / TRAINING PERIODS
train_start = "2015-01-01"
train_end = "2021-12-31"
test_start = "2022-01-01"
test_end = "2026-07-31"

def metrics(lookbacks, Ns):

    results = []

    for lookback in lookbacks:
        for N in Ns:
            signals, weights = run_strategy(lookback, N)

            returns = run_backtest(signals, weights, N)

            train_returns = returns.loc["2016-02-29":"2021-12-31"]

            #METRICS
            #SHARPE RATIO - assuming r.f.r of 0%
            sharpe = (train_returns.mean() / train_returns.std()) * np.sqrt(12)

            #ANNUALISED RETURN
            yrs = len(train_returns) / 12
            growth = (1 + train_returns).prod()
            annualised_return = growth ** (1/yrs) - 1

            #MAXIMUM DRAWDOWN
            val = (1 + train_returns).cumprod()
            curr_max = val.cummax()
            drawdown = val / curr_max - 1
            max_drawdown = drawdown.min()

            results.append({"Lookback Period" : lookback, "N" : N, "Sharpe Ratio": sharpe, "Annualised Return": annualised_return, "Maximum Drawdown": max_drawdown})

    return pd.DataFrame(results)

#PARAMETERS
lookbacks = [3, 6, 9, 12]
Ns = [10, 15, 20, 25]

results = metrics(lookbacks, Ns)
print(results.to_string(index=False))