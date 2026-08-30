import pandas as pd
import numpy as np
import matplotlib as plt

#IMPORT PRICES FROM DATA
monthly_prices = pd.read_csv("data/ftse100current_clean", index_col = 0, parse_dates = True)
monthly_returns = monthly_prices.pct_change()

#DATE RANGE
date_range = ("2016-01-31", "2026-07-31")

def run_strategy(lookback_period, N):

    #MOMENTUM 
    momentum = monthly_prices.shift(1) / monthly_prices.shift(lookback_period) - 1
    all_dates = momentum.dropna(how="all").index
    dates = all_dates[(all_dates >= date_range[0]) & (all_dates <= date_range[-1])]

    #WEIGHTS AND SIGNAL MATRICES
    weights = pd.DataFrame(0.0, index=dates, columns = monthly_prices.columns)
    signals = pd.DataFrame(0, index=dates, columns = monthly_prices.columns)

    #IMPLEMENTING STRATEGY
    for date in dates:
        curr_momentum = momentum.loc[date].dropna()
        rank_momentum = curr_momentum.sort_values(ascending=False)
        top_N = rank_momentum.head(N)

        signal = pd.Series(0, index=monthly_prices.columns)
        signal.loc[top_N.index] = 1
        signals.loc[date] = signal

        month_weights = signal / signal.sum()
        weights.loc[date] = month_weights

    return signals, weights