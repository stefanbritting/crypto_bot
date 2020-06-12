# https://towardsdatascience.com/an-introductory-example-of-bayesian-optimization-in-python-with-hyperopt-aae40fff4ff0
import numpy as np
from hyperopt import hp, tpe, Trials, fmin

class Optimizer():
# using bayesian optimizer
    def __init__(self,func ,domain_space, max_evals = 10):
        """
            function FUNC
                function to be minimized
            domain_space list of DICTs 
                range of values that should be tested for each variable
                [{"var_name": "x", "lower_bound": -4, "upper_bound": 6}, {}, ...]
            max_evals INT
                maximum number of optimazation iterations
        """
        self.func       = func
        # optimizing for FLOAT values
        #self.space      = hp.uniform('x', 36, 200)
        # optimizing for Integer values
        self.space      = hp.quniform('my_param', 36, 200, q=1)
        self.algorithm  = tpe.suggest # creating algorithm
        self.trials     = Trials() # to check records
        self.max_evals  = max_evals
        
    
    def objective_function(self, func): #  if more inputs *args
        pass
    
    def start(self):
        best_result = fmin(fn=self.func, space = self.space, algo = self.algorithm, trials = self.trials, max_evals = self.max_evals)
        print(best_result)
        return best_result
##################### End of Class ##################### 
# Example functions for 1 dimensional optimization
def poly_func(x):
    """Objective function to minimize"""
    
    # Create the polynomial object
    f = np.poly1d([1, -2, -28, 28, 12, -26, 100])

    # Return the value of the polynomial
    return f(x) * 0.05

