import random
import csv
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
        
        print("-------------- Trade Nr:" + str(len(Trade.trades)))
        print(self)
    
    def __str__(self):
        return "{oder_type} - {currency} | amount:{amount} price:{price}".format(oder_type   = self.order_type,
                                    currency    = self.currency,
                                    amount      = self.amount,
                                    price       = self.price)
    @classmethod
    def save_as_csv(cls):
        
        with open('trades.csv', 'w', newline='') as csvfile:
            fieldnames = ["timestamp", "order_type", "currency", "amount", "price", "id"] # relevant attributes for documentation
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in Trade.trades:
                writer.writerow(item.__dict__)