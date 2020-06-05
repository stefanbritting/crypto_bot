from Simulation import Simulation as Sim

sim = Sim(start_date="18-01-01", balance={"euro": 100, "btc": 0}, av_balance = 0.8)
sim.start() 