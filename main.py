from Simulation import Simulation as Sim

sim = Sim(start_date="19-12-01", balance={"euro": 300, "btc": 0}, av_balance = 0.8, stake_amount=50)
sim.start() 