import random
class Trade():
    trades = [] # list of all trade objects
    def __init__(self, timestamp, order_type, currency, amount, price):
        self.timestamp  = timestamp
        self.order_type = order_type
        self.currency   = currency
        self.amount     = amount
        self.price      = price
        self.id         = random.randrange(1000000,9999999)
        Trade.trades.append(self)