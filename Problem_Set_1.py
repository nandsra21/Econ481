# exercise zero
def github() -> str:
    """
    my github repo
    """

    return "https://github.com/nandsra21/Econ481/blob/main/Problem_Set_1.py"

# exercise one
import numpy
import pandas
import scipy
import seaborn
import matplotlib

# exercise two
def evens_and_odds(n: int) -> dict:
    """
    Returns dictionary.

    Testing:
    evens_and_odds(4) yields {'evens': 2, 'odds': 4}
    """
    dict = {'evens': 0, 'odds': 0}
    for i in range(0, n):
        if (i % 2 == 0):
            dict["evens"] = dict["evens"] + i
        else:
            dict["odds"] = dict["odds"] + i

    return dict

# exercise three
from typing import Union
from datetime import datetime, date, time, timedelta

def time_diff(date_1: str, date_2: str, out: str) -> Union[str,float]:
    """
    For example, time_diff('2020-01-01', '2020-01-02', 'float') should return

    1
    For example, time_diff('2020-01-03', '2020-01-01', 'string') should return
    
    "There are 2 days between the two dates"
    """
    date_1 = datetime.strptime(date_1, '%Y-%m-%d')
    date_2 = datetime.strptime(date_2, '%Y-%m-%d')

    diff = abs((date_1 - date_2).days)

    if out == 'float':
        return diff
    elif out == 'string':
        return f"There are {diff} days between the two dates"
    else:
        return diff
    
# exercise four
def reverse(in_list: list) -> list:
    """
    Reverse list
    """
    return in_list[::-1]

# exercise five
def prob_k_heads(n: int, k: int) -> float:
    """
    Takes as its arguments natural numbers n and k with n>k and returns the probability of getting k heads from n flips
    """
    n_minus_k_fac = 1
    for i in range(1,n-k+1):
        n_minus_k_fac *= i
    n_choose_k = 1
    for i in range(k+1, n+1):
        n_choose_k *= i
    n_choose_k /= n_minus_k_fac
    return n_choose_k * (0.5 ** k) * ((1 - 0.5) ** (n - k))
