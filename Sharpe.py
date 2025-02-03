import numpy as np
import pandas as pd

from kelly import *

def sharpe_ratio(returns, risk_free_rate=0.001/365, annualization_factor=365):
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

def get_sharpe() -> Dict[str, float]:
    data_dict = data_load()
    kelly_dict = gen_kelly()
    sharpe_dict = {}
    for sym in data_dict.keys():
        sharpe = sharpe_ratio(data_dict[sym].close)
        sharpe_kelly = sharpe_ratio(kelly_dict[sym].kelly)
        sharpe_dict[sym] = sharpe
        sharpe_dict[f"{sym}_kelly"] = sharpe_kelly
    return sharpe_dict

if __name__ == '__main__':
    get_sharpe()
