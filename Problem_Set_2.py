# Exercise 0
def github() -> str:
    """
    my github repo
    """

    return "https://github.com/nandsra21/Econ481/blob/main/Problem_Set_2.py"

# Exercise 1
import numpy as np

def simulate_data(seed: int = 481) -> tuple:
    """
    returns 1000 simulated observations via the following data generating process:
    y_i = 5 + 3x_{i1} + 2x_{i2} + 6x_{i3} + \varepsilon_i
    takes one argument, seed, an integer that is used to set a seed (this should default to 481 if not provided), and should return a tuple of two elements, (y,X) where y is a np.array and X is a np.array.
    """
    np.random.seed(seed)

    X = np.random.standard_normal(size=(1000, 3))

    epsilon = np.random.standard_normal(size=(1000, 1))

    y = 5 + 3 * X[:, 0] + 2 * X[:, 1] + 6 * X[:, 2] + epsilon.flatten()
    
    return y.reshape(-1,1), X

y, X = simulate_data()

# Exercise 2
from scipy.optimize import minimize

def negative_log_likelihood(params, y, X):
    beta_0, beta_1, beta_2, beta_3 = params
    predicted_y = beta_0 + beta_1 * X[:, 0] + beta_2 * X[:, 1] + beta_3 * X[:, 2]
    residuals = y - predicted_y
    nll = 0.5 * np.log(2 * np.pi) + np.log(np.std(residuals)) + 0.5 * np.mean(residuals ** 2)
    return nll
    
def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    Some docstring
    """
    initial_guess = np.zeros(4)
    result = minimize(negative_log_likelihood, initial_guess, args=(y.flatten(), X))
    return result.x

estimate_mle(y, X)
# Exercise 3
def loss_function(params, X, y):
    beta_0, beta_1, beta_2, beta_3 = params
    predicted_y = beta_0 + beta_1 * X[:, 0] + beta_2 * X[:, 1] + beta_3 * X[:, 2]
    residuals = y - predicted_y
    return np.sum(residuals ** 2)
    
def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    some docstring
    """
    initial_guess = np.zeros(4)
    result = minimize(loss_function, initial_guess, args=(X, y.flatten()))
    return result.x

estimate_ols(y,X)
