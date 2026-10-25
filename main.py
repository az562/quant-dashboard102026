import yfinance as yf
import pandas as pd
import numpy as np

TICKERS = ["SPY", "QQQ", "TLT"]
START = "2020-01-01"
BENCHMARK = "SPY"

def fetch_data(tickers, start):
    data = yf.download(tickers, start=start, auto_adjust=True)["Close"]
    return data.dropna()

def calculate_metrics(returns, benchmark_returns=None):
    metrics = {}
    metrics["ann_vol"] = returns.std() * np.sqrt(252)
    metrics["sharpe"] = (returns.mean() * 252) / metrics["ann_vol"] if metrics["ann_vol"] != 0 else 0
    
    cum = (1 + returns).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    metrics["max_dd"] = drawdown.min()
    
    if benchmark_returns is not None:
        cov = np.cov(returns, benchmark_returns)[0, 1]
        var = benchmark_returns.var()
        metrics["beta"] = cov / var if var != 0 else 0
    
        # Dodatkowe metryki
    metrics["total_return"] = (1 + returns).prod() - 1
    metrics["win_rate"] = (returns > 0).mean()
    metrics["avg_win"] = returns[returns > 0].mean() if (returns > 0).any() else 0
    metrics["avg_loss"] = returns[returns < 0].mean() if (returns < 0).any() else 0
    return metrics

def simple_backtest(prices, fast=20, slow=50):
    sma_fast = prices.rolling(fast).mean()
    sma_slow = prices.rolling(slow).mean()
    signal = (sma_fast > sma_slow).astype(int)
    returns = prices.pct_change()
    strategy_returns = signal.shift(1) * returns
    return strategy_returns.dropna()

if __name__ == "__main__":
    print("Pobieranie danych...")
    prices = fetch_data(TICKERS, START)
    returns = prices.pct_change().dropna()
    
    results = {}
    for ticker in TICKERS:
        print(f"Backtest: {ticker}")
        strat_ret = simple_backtest(prices[ticker])
        results[ticker] = calculate_metrics(strat_ret, returns[BENCHMARK])
    
    df = pd.DataFrame(results).T
    df.to_csv("data/latest_metrics.csv")
    print("\nWyniki:")
    print(df.round(4))
        # Wykres equity curve
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    for ticker in TICKERS:
        strat_ret = simple_backtest(prices[ticker])
        equity = (1 + strat_ret).cumprod()
        plt.plot(equity.index, equity.values, label=ticker)
    plt.title("Equity Curve - SMA 20/50")
    plt.legend()
    plt.grid(True)
    plt.savefig("reports/equity_curve.png", dpi=150, bbox_inches="tight")
    print("Zapisano wykres: reports/equity_curve.png")
    print("\nZapisano do data/latest_metrics.csv")