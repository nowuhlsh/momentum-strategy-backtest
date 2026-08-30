import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib as plt

monthly_prices = pd.read_csv("data/ftse100current_clean", index_col = 0, parse_dates = True)

print(monthly_prices.shape)