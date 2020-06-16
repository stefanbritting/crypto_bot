# https://towardsdatascience.com/an-introductory-example-of-bayesian-optimization-in-python-with-hyperopt-aae40fff4ff0
import numpy as np
from hyperopt import hp, tpe, Trials, fmin, STATUS_OK
import csv
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
            parameter list
                list of parameters {}
        """
        self.func       = func
        # optimizing for FLOAT values
        #self.space      = hp.uniform('x', 36, 200)
        # optimizing for Integer values
        self.space      = domain_space
        self.algorithm  = tpe.suggest # creating algorithm
        self.trials     = Trials() # to check records
        self.max_evals  = max_evals
        
    
    def objective_function(self, func): #  if more inputs *args
        pass
    
    def start(self):
        best_result = fmin(fn=self.func, space = self.space, algo = self.algorithm, trials = self.trials, max_evals = self.max_evals)
        print(best_result)
        
        ################ Documentation ################ 
        temp_doc = ["#### Best Result ####", str(best_result) ]
        Optimizer.__write_to_csv(temp_doc)
        i = 0
        for item in self.trials.results:
            item["values"] = self.trials.trials[i]["misc"]["vals"] 
            Optimizer.__write_to_csv(str(item))
            i = i + 1
        
        Optimizer.__write_to_csv(["-------------------------------------------------"])
        return best_result
        
    @staticmethod
    def __write_to_csv(text):
        with open('crypto_bot/optimize/results.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(str(text))

##################### End of Class ##################### 
# Example functions for 1 dimensional optimization
def poly_func(x):
    """Objective function to minimize"""
    
    # Create the polynomial object
    f = np.poly1d([1, -2, -28, 28, 12, -26, 100])

    # Return the value of the polynomial
    return f(x) * 0.05

