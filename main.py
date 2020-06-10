from Simulation import Simulation as Sim

sim = Sim(start_date="19-12-01", balance={"euro": 1000, "btc": 0}, av_balance = 0.8, stake_amount=50, stop_loss = 0.02)
sim.start() 