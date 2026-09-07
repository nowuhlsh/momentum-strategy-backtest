# FTSE 100 Momentum Strategy Backtest

## Motivation

## Research Question
Does a 12-2 momentum strategy generate positive returns among *current* FTSE 100 constituents, relative to an equally weighted benchmark?

The analysis evaluates performance using annualised return, Sharpe ratio and maximum drawdown.

## Methodology

### Data
The universe for this strategy was the FTSE 100 Constituents as of August 1, 2026. Although this does result in survivorship bias affecting our results, for future projects I'd like to consider this in the model with more experience!

Historical market data was obtained from **Yahoo Finance**. Raw market data is not included in this repository. The analysis is presented for research/educational purposes, and users wishing to reproduce the analysis should obtain the data directly from the relevant data provider and review its applicable terms of use.

Some examples of EDA applied:
* LSE ticker conventions were standardised where required (for example, BT.A was mapped to BT-A for Yahoo Finance).
* Price data was retained only where the available price history corresponded to trading on the LSE. EDV was excluded before June 2021 as this data was related to its prior Toronto listing.

THe backtest covers 01-01-2015 - 01-08-2025.

### Momentum Signal
The signal is based on **12-2 total-return momentum**. As the data is adjusted for dividends and stock shares, for stock \(i\) at month \(t\) the signal is calculated as:

$$
M_{i,t} = \frac{P_{i,t-1}}{P_{i,t-12}} - 1
$$

where:
* \(M_{i,t}\) = momentum signal for stock \(i\) at month \(t\)
* \(P_{i,t-1}\) = adjusted price at the end of the most recent completed month
* \(P_{i,t-12}\) = adjusted price 12 months previously


### Constructing portfolios
At the beginning of each month, eligible stocks are ranked according to their momentum signal. The strategy selects the top *N* stocks with the highest momentum values. The selected stocks are assigned equal weights:

$$
w_{i,t} = \frac{1}{N}
$$

where \(N\) is the number of stocks selected, and we test different values later down the line.

The portfolio is rebalanced monthly, and the return of the portfolio for month \(\t) is calculated as the weighted sum of the stock returns.

It is vital that the momentum signal is aligned properly with the date of the returns to avoid **look-ahead bias**. For example, a signal formed from returns known at the end of January should not form a portfolio that generates returns over January.

### Benchmark
To provide a comparison for the strategy, an equally weighted benchmark is constructed. The benchmark just assigns equal weights to each eligible stock at that rebalancing, giving a baseline for whether the selected stocks generate meaningful returns.

### Transaction Costs
Transaction costs are incorporated to make the backtest more representative of a realistic strategy, especially for a momentum strategy where there is a high turnover each month. Research informed the assumption of a **0.5 Stamp Duty Reserve Tax (SDRT) on purchases** with **no cost associated with selling a stock**.

Turnover at each rebalancing was calculated using the signals matrix. The sum of the absolute values of the row vector formed by the subtraction of row \(t-1\) and \(t\) gives the number of turnovers. As there is a constant number of stocks in the portfolio, it is apparent that every sale demands a purchase. Therefore the number of purchases is equal to half the turnover. Note that the first month of the backtest demands *N* purchases.

## Backtest design
### Training 
Two strategy parameters are test over a training period: 01-01-2015 - 




