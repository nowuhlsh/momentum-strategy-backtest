# FTSE 100 Momentum Strategy Backtest
This project looks at backtesting a simple 12-2 month total-return momentum strategy on the current constituents of the FTSE 100 exchange as of *2026/08/01*, and analysing its performance compared to an equal-weighted universe investment strategy.

### Motivation
As a mathematics student, I'm interested in how areas like the financial sector can use data and quantitative analysis to optimise their strategies and turn data into real-life decision-making. Although this backtest has limitations as stated later in the document, this project was really interesting to build as it has demanded data analysis, programming and some financial knowledge. I hope in the future to build upon these skills and use them to tackle the limitations to make it even more realistic.

## Methodology
### Universe
The universe on which this strategy is used is the FTSE 100 constituents as of *2026/08/01*. The limitation this poses is potential for survivorship bias: we don't face the threat of investing in companies that left the exchange or no longer exist. For a future project, I would like to source an even more complex source of data which can indicate the time of entry and exit from the exchange. To be clear, the data I used was data only pertained from the company whilst it was listed on the London Stock Exchange (LSE).

### Data
The data I used is sourced from Yahoo Finance. By no means is this project intended for trading or investing purposes or advice, it is for informational and exploratory purposes only.

Upon extracting the daily adjusted close prices, using *Pandas* I first resampled the data to reflect the monthly close price for each stock. Then, checking for duplicates, missing values and large swings were vital - this could imply an acquistition or stock split took place and may have to be adjusted for, although this did not occur in the data.

Additionally, after checking for missing values I needed to research the company's history on the exchange and found two particular cases of data that would need to be adjusted. Pershing Square Holdings (PSH) officially entered the LSE on 2 May 2017, but had data during the months of March and April from its listing on the Euronext Amsterdam. I chose to exclude these months as the backtest should only use prices on the LSE.

Secondly, Endeavour Mining plc (EDV) had prices from before its listing on the LSE on 14 June 2021, and therefore prices before this were discarded accordingly.

### Strategy
The strategy itself is a 12-2 month total-return momentum strategy. This means that we first had to calculate the momentum for each company, every month. This was done by the calculation: 

$$ 
M_{t} = \frac{p_{t-2}}{p_{t-12}} - 1
$$
where $M_{t}$ denotes the momentum at month $t$, $p_{t-2}$ denotes the share price at month $t-2$, and $p_{t-12}$ denotes the share price at month $t-12$. This means that we are calculating the change in price over the year, and we use 2 months in the past to avoid short-term reversal - over a short time horizon outliers tend to reverse. 
















