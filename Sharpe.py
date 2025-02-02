import numpy as np
import pandas as pd

def sharpe_ratio(returns, risk_free_rate=0.0, annualization_factor=252):
    """
    Calculates the Sharpe Ratio.

    Args:
        returns (pd.Series or np.array): A series or array of returns.  Crucially, these should be *periodic* returns (daily, weekly, etc.)
        risk_free_rate (float, optional): The risk-free rate of return. Defaults to 0.0.  Should be in the same periodicity as the returns.
        annualization_factor (int, optional): The number of periods in a year. Defaults to 252 (trading days).

    Returns:
        float: The Sharpe Ratio.  Returns NaN if the standard deviation of returns is zero.
    """

    if isinstance(returns, pd.Series):
      returns = returns.values # Convert pandas Series to numpy array for calculations

    excess_returns = returns - risk_free_rate
    mean_excess_return = np.mean(excess_returns)
    std_dev_excess_return = np.std(excess_returns)

    if std_dev_excess_return == 0:
        return np.nan  # Handle the case where standard deviation is zero to avoid division by zero.
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


# Important notes on Risk-Free Rate and Annualization:

# * Risk-Free Rate: The risk-free rate MUST be expressed in the same periodicity as your returns data.
#   If your returns are daily, your risk-free rate must be a *daily* risk-free rate.  A common mistake is to use an annual risk-free rate directly with daily returns.  Divide the annual risk-free rate by the number of periods in the year to get the per-period risk-free rate.  For example, if the annual risk-free rate is 2%, the daily risk-free rate is approximately 0.02 / 252.

# * Annualization Factor: The annualization factor is used to scale the Sharpe Ratio to an annual basis.  
#   - For daily data, use 252 (trading days) or 365 (calendar days). 252 is more common.
#   - For weekly data, use 52.
#   - For monthly data, use 12.

# * Returns: Your 'returns' data *must* be the percentage or decimal change in value (e.g., (price_end - price_begin) / price_begin), *not* the absolute price.

# * Zero Standard Deviation: The code now handles the case where the standard deviation of returns is zero, which would lead to division by zero, by returning NaN. This is a more robust approach.

# * Pandas Series vs. NumPy Array: While the function works with both, using a Pandas Series for your returns data is generally recommended.  Pandas provides better data handling and alignment capabilities, which are very useful in financial analysis.  I've added a conversion inside the function to handle Series input smoothly.
