from Data               import Data
from Strategy           import Strategy
from Account            import Account
from Simulation         import Simulation as Sim
from hyperopt           import hp
from optimize.optimize  import Optimizer, poly_func

def opt_wrapper(params):
    """
        optimizing for periods
    """
    # assign parameters
    periods     = int(params[0]) # space from optimizer returns floats
    adx_value   = int(params[1])
    
    ###### Define Simulations ###### 
    data        = Data(start_date="19-12-01") # historical data interfal: hours
    df          = data.load()
    strategy    = Strategy(df=df, periods = periods, adx_value = adx_value) 
    account     = Account(balance={"euro": 1000, "btc": 0}, av_balance = 0.8)
    
    sim = Sim(strategy = strategy, account = account, stake_amount=50, stop_loss = 0.02)
    sim_result = sim.start() 
    
    # negate as optimization looks for a minimum
    sim_result = - sim_result["account"].balance["euro"]
    
    return sim_result
    
"""
test = normal_sim()
"""
############# Parameter for Hyper-Parameter-Tuning ############# 
# defining variables and their spaces
domain_space    = [hp.quniform('periods', 36, 800, q=1), hp.quniform('adx_value', 20, 26, q=1)]

optimizer       = Optimizer(func = opt_wrapper, domain_space = domain_space, max_evals=40)

test = optimizer.start()
print(test)

#########################################################################################

def normal_sim():
    data        = Data(start_date="19-12-01") # historical data interfal: hours
    df          = data.load()
    strategy    = Strategy(df=df, periods = 47) 
    account     = Account(balance={"euro": 1000, "btc": 0}, av_balance = 0.8)
    
    sim = Sim(strategy = strategy, account = account, stake_amount=50, stop_loss = 0.02)
    sim_result = sim.start() 
    
    return sim_result
