import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.integrate import quad
from scipy.stats import norm
from typing import Dict, Callable
from symbols import *

def data_load() -> Dict[str, pd.DataFrame]:
    data_dict = {}
    for sym in symbols:
        data = pd.read_csv("./{sym}.csv")
        data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y")
        data_dict[sym] = data
    return data_dict

def norm_integral(f:Callable, mean:float, std:float) -> float:
    val, er = quad(
        lambda s: np.log(1 + f * s) * norm.pdf(s, mean, std),
        mean - 3 * std,
        mean + 3 * std,
    )
    return -val

def get_kelly(data:pd.DataFrame) -> np.ndarray:
    solution = minimize_scalar(
        norm_integral, 
        args=(data["mean"], data["std"]),
        bounds=[0, 2],
        method="bounded"
    )
    return np.array(solution.x)

def gen_kelly() -> Dict[str, pd.DataFrame]:
    data_dict = data_load()
    kelly_dict = {}
    for sym, data in data_dict.items:
        X = data["close"].resample('D').last().pct_change().dropna()
        Y = X.copy()
        X = X.rolling(25).agg(["mean", "std"]).dropna
        X = X.apply(get_kelly, axis=1)
        Kelly = Y.mul(X.shift()).dropna().add(1).cumprod().sub(1)
        kelly_dict[sym] = pd.DataFrame({"date": data["date"], "close": data["close"], "kelly": Kelly}, columns=["date","close","kelly"])

    return kelly_dict

if '__name__' == '__main__':
    gen_kelly()
