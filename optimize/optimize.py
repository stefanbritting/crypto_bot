# https://towardsdatascience.com/an-introductory-example-of-bayesian-optimization-in-python-with-hyperopt-aae40fff4ff0
import numpy as np
from hyperopt import hp

class Optimizer():
# using bayesian optimizer
    def __init__(self):
        self.space = hp.uniform('x', -5, 6)
    
    def objective_function(self, func): #  if more inputs *args
        pass
    
    def start(self):
        pass
##################### End of Class ##################### 

def poly_func(x):
    """Objective function to minimize"""
    
    # Create the polynomial object
    f = np.poly1d([1, -2, -28, 28, 12, -26, 100])

    # Return the value of the polynomial
    return f(x) * 0.05