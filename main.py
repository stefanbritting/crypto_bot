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
    periods_bol     = int(params[0]) # space from optimizer returns floats
    periods_adx     = int(params[1])
    periods_rsi     = int(params[2])
    adx_value       = int(params[3])
    
    ###### Define Simulations ###### 
    data        = Data(start_date="20-03-01") # historical data interfal: hours
    df          = data.load()
    strategy    = Strategy(df=df, periods_bol = periods_bol,periods_adx = periods_adx,periods_rsi = periods_rsi, adx_value = adx_value)
    
    account     = Account(balance={"euro": 1000, "btc": 0}, av_balance = 0.8)
    
    sim = Sim(strategy = strategy, account = account, stake_amount=50, stop_loss = 0.02)
    sim_result = sim.start() 
    
    # negate as optimization looks for a minimum
    sim_result = - sim_result["account"].balance["euro"]
    
    return sim_result
    



############# Parameter for Hyper-Parameter-Tuning ############# 
# defining variables and their spaces

domain_space    = [hp.quniform('periods_bol', 10, 800, q=1), hp.quniform('periods_adx', 10, 800, q=1), hp.quniform('periods_rsi', 5, 35, q=1), hp.quniform('adx_value', 20, 26, q=1)]

optimizer       = Optimizer(func = opt_wrapper, domain_space = domain_space, max_evals=1)

test = optimizer.start()
print(test)

#########################################################################################

def normal_sim():
    data        = Data(start_date="19-12-01") # historical data interfal: hours
    df          = data.load()
    strategy    = Strategy(df=df, periods_bol = 760, periods_adx = 56,periods_rsi = 10, adx_value = 20)
    account     = Account(balance={"euro": 1000, "btc": 0}, av_balance = 0.8)
    
    sim = Sim(strategy = strategy, account = account, stake_amount=50, stop_loss = 0.02)
    sim_result = sim.start() 
    
    return sim_result
    
#