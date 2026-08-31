import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
train_start = "2016-02-29"
train_end = "2021-12-31"
test_start = "2022-01-01"
test_end = "2026-07-31"

def metrics(lookbacks, Ns, date_start, date_end):

    results = []

    for lookback in lookbacks:
        for N in Ns:
            signals, weights = run_strategy(lookback, N)

            returns = run_backtest(signals, weights, N)
            period_returns = returns.loc[date_start:date_end]
            
            #METRICS
            #SHARPE RATIO - assuming r.f.r of 0%
            sharpe = (period_returns.mean() / period_returns.std()) * np.sqrt(12)

            #ANNUALISED RETURN
            yrs = len(period_returns) / 12
            growth = (1 + period_returns).prod()
            annualised_return = growth ** (1/yrs) - 1

            #MAXIMUM DRAWDOWN
            val = (1 + period_returns).cumprod()
            curr_max = val.cummax()
            drawdown = val / curr_max - 1
            max_drawdown = drawdown.min()

            results.append({"Lookback Period" : lookback, "N" : N, "Sharpe Ratio": sharpe, "Annualised Return": annualised_return, "Maximum Drawdown": max_drawdown})

    return pd.DataFrame(results), period_returns

#PARAMETERS
lookbacks = [3, 6, 9, 12]
Ns = [10, 15, 20, 25]

train_results, train_returns = metrics(lookbacks, Ns, train_start, train_end)
print(train_results.to_string(index = False))
print("\nRanked by Sharpe Ratio")
print(train_results.sort_values(by = "Sharpe Ratio", ascending = False).head(5).to_string(index = False))
print("\nRanked by Maximum Drawdown")
print(train_results.sort_values(by = "Maximum Drawdown", ascending = False).head(5).to_string(index = False))
print("\nRanked by Annualised Return")
print(train_results.sort_values(by = "Annualised Return", ascending = False).head(5).to_string(index = False))

#TEST USING DECIDED STRATEGY PARAMETERS
chosen_lookback = [9]
chosen_n = [20]

test_results, test_returns = metrics(chosen_lookback, chosen_n, test_start, test_end)
print("\nTest Results")
print(test_results.to_string(index = False))

#GETTING BENCHMARK
benchmark_returns = monthly_returns.mean(axis=1).loc[test_start:test_end]

#sharpe ratio
bm_sharpe = (benchmark_returns.mean() / benchmark_returns.std()) * np.sqrt(12)

#annualised return
bm_yrs = len(benchmark_returns) / 12
bm_growth = (1 + benchmark_returns).prod()
bm_annualised_return = bm_growth ** (1/bm_yrs) - 1

#maximum drawdown
bm_val = (1 + benchmark_returns).cumprod()
bm_curr_max = bm_val.cummax()
bm_drawdown = bm_val / bm_curr_max - 1
bm_max_drawdown = bm_drawdown.min()

print("\nEqual-weight Universe-matched Benchmark")
bm_metrics = {"Sharpe Ratio": bm_sharpe, "Annualised Return": bm_annualised_return, "Maximum Drawdown": bm_max_drawdown}
for metric, value in bm_metrics.items():
    print(f"{metric}: {value:6f}")

capital = 10000
benchmark_value = capital * (1 + benchmark_returns).cumprod()
test_value = capital * (1 + test_returns).cumprod()
plt.plot(benchmark_returns.index, benchmark_value, label = "Benchmark")
plt.plot(test_returns.index, test_value, label = "Strategy")
plt.legend()
plt.show()
