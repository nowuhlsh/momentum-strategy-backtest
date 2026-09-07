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

The backtest covers 31-01-2015 - 31-07-2026.

### Momentum Signal
The signal is based on **12-2 total-return momentum**. As the data is adjusted for dividends and stock shares, for stock $\(i\$) at month $\(t\)$ the signal is calculated as:

$$
M_{i,t} = \frac{P_{i,t-1}}{P_{i,t-12}} - 1
$$

where:
* $\(M_{i,t}\)$ = momentum signal for stock $\(i\)$ at month $\(t\)$
* $\(P_{i,t-1}\)$ = adjusted price at the end of the most recent completed month
* $\(P_{i,t-12}\)$ = adjusted price 12 months previously


### Constructing portfolios
At the beginning of each month, eligible stocks are ranked according to their momentum signal. The strategy selects the top *N* stocks with the highest momentum values. The selected stocks are assigned equal weights:

$$
w_{i,t} = \frac{1}{N}
$$

where $\(N\)$ is the number of stocks selected, and we test different values later down the line.

The portfolio is rebalanced monthly, and the return of the portfolio for month $\(t\)$ is calculated as the weighted sum of the stock returns.

It is vital that the momentum signal is aligned properly with the date of the returns to avoid **look-ahead bias**. For example, a signal formed from returns known at the end of January should not form a portfolio that generates returns over January.

### Benchmark
To provide a comparison for the strategy, an equally weighted benchmark is constructed. The benchmark just assigns equal weights to each eligible stock at that rebalancing, giving a baseline for whether the selected stocks generate meaningful returns.

### Transaction Costs
Transaction costs are incorporated to make the backtest more representative of a realistic strategy, especially for a momentum strategy where there is a high turnover each month. Research informed the assumption of a **50 bps Stamp Duty Reserve Tax (SDRT) on purchases** with **no cost associated with selling a stock**.

Turnover at each rebalancing was calculated using the signals matrix. The sum of the absolute values of the row vector formed by the subtraction of row $\(t-1\)$ and $\(t\)$ gives the number of turnovers. As there is a constant number of stocks in the portfolio, it is apparent that every sale demands a purchase. Therefore the number of purchases is equal to half the turnover. Note that the first month of the backtest demands *N* purchases.

## Backtest design
### Training 
Two strategy parameters are tested over a training period with data from: 31-01-2015 - 31-12-2021, with the portfolio generating returns starting 29-02-2016 to ensure that even when lookback period changed the trading began at the same date.

The parameters considered:
* Momentum lookback period - 3, 6, 9, 12 months
* Number of stocks selected - 10, 15, 20, 25

The purpose of the training period being to identify a suitable strategy specification before evaluating its performance on a out-of-sample testing period. Once strategy specifications were chosen, they are tested only once out-of-sample to avoid trying to evaluate a strategy by using parameters selected using information from the testing period.

### Testing
The test was performed from dates 31-01-2022 - 31-07-2026, and evaluated using three performance metrics.

#### Sharpe Ratio
Sharpe ratio measures the return generated relative to the volatility of the returns. A higher Sharpe ratio indicates greater return per unit of risk, and annualised Sharpe ratio is calculated by:

$$
Sharpe =
\frac{R_p-R_f}
{\sigma_p}
\sqrt{12}
$$

where:
*  $\(R_p\)$ = portfolio return over period
*  $\(R_f\)$ = risk-free rate
*  $\(\sigma_p\)$ = standard deviation over period
*  $\(\sqrt{12}\)$ annualises the monthly calculation

Risk-free rate of 0% was assumed.

Sharpe ratio was the primary metric, but two secondary metrics were used.

#### Maximum Drawdown
Maximum drawdown measures the largest peak-to-trough decline in portfolio value, providing an indication on volatility and risk.

#### Annualised Return
Annualised return measures the annual rate of return generated by the strategy, providing an indication of absolute perfomance unlike Sharpe ratio. This is useful as a very high Sharpe Ratio is futile if the strategy returns next to nothing. It is calculated by:

$$
R_{\text{annualised}} =
\left(
\prod_{t=1}^{T} (1 + R_t)
\right)^{\frac{12}{T}} - 1
$$

where:
* $\(R_t\)$ is the return in month $t$
* $T$ is the number of monthly observations

### 










