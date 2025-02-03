import numpy as np
import pandas as pd

def sharpe_ratio(returns, risk_free_rate=0.0, annualization_factor=252):
    if isinstance(returns, pd.Series):
      returns = returns.values 

    excess_returns = returns - risk_free_rate
    mean_excess_return = np.mean(excess_returns)
    std_dev_excess_return = np.std(excess_returns)

    if std_dev_excess_return == 0:
        return np.nan  
    else:
        sharpe = (mean_excess_return / std_dev_excess_return) * np.sqrt(annualization_factor)
        return sharpe


# Example Usage:
# 1. Using a Pandas Series (recommended):
np.random.seed(42)  # for reproducibility
daily_returns = pd.Series(np.random.normal(0.0001, 0.01, 252)) # Example daily returns (mean 0.01%, std dev 1%)
sharpe = sharpe_ratio(daily_returns, risk_free_rate=0.0001/252, annualization_factor=252) # Risk-free rate should be *per period*

print(f"Sharpe Ratio (using Pandas Series): {sharpe}")

# 2. Using a NumPy array:
daily_returns_np = np.random.normal(0.0001, 0.01, 252)
sharpe_np = sharpe_ratio(daily_returns_np, risk_free_rate=0.0001/252, annualization_factor=252)  # Risk-free rate should be *per period*
print(f"Sharpe Ratio (using NumPy array): {sharpe_np}")
