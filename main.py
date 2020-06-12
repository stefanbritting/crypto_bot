from Data               import Data
from Strategy           import Strategy
from Account            import Account
from Simulation         import Simulation as Sim

from optimize.optimize  import Optimizer, poly_func

def opt_wrapper(periods):
    """
        optimizing for periods
    """
    periods = int(periods) # space from optimizer returns floats
    
    data        = Data(start_date="20-05-01") # historical data interfal: hours
    df          = data.load()
    strategy    = Strategy(df=df, periods = periods) 
    account     = Account(balance={"euro": 1000, "btc": 0}, av_balance = 0.8)
    
    sim = Sim(strategy = strategy, account = account, stake_amount=50, stop_loss = 0.02)
    sim_result = sim.start() 
    
    # negate as optimization looks for a minimum
    sim_result = - sim_result["account"].balance["euro"]
    
    return sim_result

def normal_sim():
    data        = Data(start_date="20-05-01") # historical data interfal: hours
    df          = data.load()
    strategy    = Strategy(df=df, periods = 47) 
    account     = Account(balance={"euro": 1000, "btc": 0}, av_balance = 0.8)
    
    sim = Sim(strategy = strategy, account = account, stake_amount=50, stop_loss = 0.02)
    sim_result = sim.start() 
    
    return sim_result    

test = normal_sim()
"""
optimizer = Optimizer(func = opt_wrapper, domain_space = "test", max_evals=5)
test = optimizer.start()
print(test)
"""

