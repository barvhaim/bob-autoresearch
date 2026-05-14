# AutoResearch — Trading Strategy Optimization

> Autonomous optimization of a trading strategy to maximize Sharpe ratio.

## Domain Configuration

- **Domain**: Quantitative trading strategy
- **Target file**: `target.py` (strategy logic: signals, position sizing, risk)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score`
- **Metric direction**: **higher** is better (Sharpe ratio)
- **Time budget per run**: 3 minutes
- **Timeout**: 6 minutes

## What You CAN Do

- Change entry/exit signal logic
- Adjust position sizing
- Add/remove technical indicators
- Change lookback periods
- Modify risk management rules

## What You CANNOT Do

- Modify `evaluate.py` or `program.md`
- Change the historical data (it's in evaluate.py)
- Use future data (no look-ahead bias)
- Hard-code trade dates from the backtest period
- Import external data sources

## Adaptation Notes

Your `evaluate.py` should:
1. Load fixed historical price data (e.g., 5 years daily OHLCV)
2. Import `strategy(prices)` from target.py
3. Run backtest: simulate trades, track PnL
4. Compute Sharpe ratio = mean(returns) / std(returns) * sqrt(252)
5. Print `score: <sharpe_ratio>`

## Overfitting Warning

Add to program.md: "Strategies with >20 parameters are suspicious.
If Sharpe > 3.0 on daily data, you're probably overfitting."
