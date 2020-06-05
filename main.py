from Simulation import Simulation as Sim

sim = Sim(start_date="17-01-01", balance={"euro": 100, "btc": 0}, av_balance = 0.8, stake_amount=50)
sim.start() 