def github() -> str:
    """
    my github repo
    """

    return "https://github.com/nandsra21/Econ481/blob/main/Problem_Set_4.py"

import pandas as pd

def load_data() -> pd.DataFrame:
    """
    Some docstrings.
    """
    TSLA_df = pd.read_csv("https://lukashager.netlify.app/econ-481/data/TSLA.csv")
    TSLA_df['Date'] = pd.to_datetime(TSLA_df['Date'])
    TSLA_df.set_index("Date", inplace=True)
    TSLA_df.index = pd.to_datetime(TSLA_df.index)
    TSLA_df.sort_index(inplace=True)
    return TSLA_df

TSLA_df = load_data()

import matplotlib.pyplot as plt 
def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    """
    Some docstrings
    """

    df.index = pd.to_datetime(df.index)
    
    filtered_df = df[(df.index >= start) & (df.index <= end)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df.index, filtered_df['Close'], color='blue')
    
    plt.title(f"Closing Price between {start} and {end}")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.xticks(rotation=45)
    
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_close(TSLA_df)

import statsmodels.api as sm

def autoregress(df: pd.DataFrame) -> float:
    """
    Some docstrings.
    """
    val_df = df.copy()
    val_df['delta_x'] = val_df['Close'].diff(periods=1)
    val_df['lagged_delta_x'] = val_df['delta_x'].shift(freq=pd.Timedelta(days=1))
    val_df.dropna(subset=['delta_x', 'lagged_delta_x'], inplace=True)

    X = val_df['lagged_delta_x']
    y = val_df['delta_x']
    model = sm.OLS(y, X)
    results = model.fit(cov_type='HC1')
    t_stat_beta_0 = results.tvalues['lagged_delta_x']

    return t_stat_beta_0

autoregress(TSLA_df)

import pandas as pd
import numpy as np
import statsmodels.api as sm

def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Some docstring=
    """
    val_df = df
    val_df['delta_x'] = val_df['Close'].diff()
    val_df['y'] = (val_df['delta_x'] > 0).astype(int)
    val_df['lagged_delta_x'] = val_df['delta_x'].shift(1)

    val_df.dropna(subset=['y', 'lagged_delta_x'], inplace=True)

    X = val_df['lagged_delta_x']
    y = val_df['y']
    model = sm.Logit(y, X)
    results = model.fit()

    t_stat_beta_0 = results.tvalues["lagged_delta_x"]

    return t_stat_beta_0

autoregress_logit(TSLA_df)

def plot_delta(df: pd.DataFrame) -> None:
    """
    Some docstrings.
    """
    df['delta_x'] = df['Close'].diff()

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['delta_x'], color='blue', linestyle='-')
    plt.title('Differences Between Consecutive Values')
    plt.xlabel('Date')
    plt.ylabel('Delta_x')
    plt.grid(True)
    plt.show()

plot_delta(TSLA_df)