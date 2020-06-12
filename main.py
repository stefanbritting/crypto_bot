from Simulation import Simulation as Sim
from optimize.optimize import Optimizer

sim = Sim(start_date="20-04-01", balance={"euro": 1000, "btc": 0}, av_balance = 0.8, stake_amount=50, stop_loss = 0.02)
test = sim.start() 

def negate_sim(func):
    """
        the optimizer is used to find a minimum
        => the outcome of the sim musst be negated if a pos maximum is to be found
        e.G. to maximize profits => just negate them 
    """
    return None

"""
optimizer = Optimizer(func = poly_func, domain_space = "test", max_evals=5)
test = optimizer.start()
print(test)
"""