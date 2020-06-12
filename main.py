from Data               import Data
from Strategy           import Strategy
from Account            import Account
from Simulation         import Simulation as Sim

from optimize.optimize  import Optimizer

data        = Data(start_date="20-04-01")
df          = data.load()
strategy    = Strategy(df=df)
account     = Account(balance={"euro": 1000, "btc": 0}, av_balance = 0.8)

sim = Sim(strategy = strategy, account = account, stake_amount=50, stop_loss = 0.02)
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

