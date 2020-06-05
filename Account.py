
class Account():
    # 
    number_of_trades = 0
    def __init__(self, balance = {}, av_balance = 0.8):
        """
        balance Dict
            {"btc:" 69, "euro": 12}
        av_balance FLOAT [0,1]
            =how much of the 'available balance' for each crypto currency (incl. euro) should be used for trading
        """
        if balance == {}:
            raise AttributeError("No balance for currencies has been set!")
        self.balance        = balance
        self.av_balance     = av_balance
        self.sec_balance    = {}
        self.trades         = []
        
        self.__split_av_balance()
        

        
    def __split_av_balance(self):
        # splits all available balances of cryptos into balance(used for trading) & sec_balance("secured", untouch amounts)
        
        for ba in self.balance:
            self.sec_balance[ba]    = self.balance[ba] * (1 - self.av_balance)
            self.balance[ba]        =  self.balance[ba] * self.av_balance
    
    def sufficient_balance(self, currency, amount):
        if self.balance[currency] >= amount and amount != 0:
            return True
        else:
            return False
    
    def execute_order(self, order_type, currency, amount, price):
        """
        Note: all orders are executed between a crypto and euro (e.g. "sell crypto")
            order_type STRING
                sell | buy
            currency STRING
                name of crypto currency
            amount FLOAT
                amount of crypto currencies
            price FLOAT
                price in euro for 1 unit of crypto currency
                
        """
        trade = None
        if order_type == "buy":
            if self.sufficient_balance("euro", amount*price) == True:
                self.balance["euro"]    = self.balance["euro"] - amount * price
                self.balance[currency]  = self.balance[currency] + amount
                
                trade = {"order_type": order_type, "currency": currency, "amount": amount, "price": price}
        elif order_type =="sell":
            if self.sufficient_balance(currency, amount) == True:
                self.balance[currency]  = self.balance[currency] - amount
                self.balance["euro"]    = self.balance["euro"] + amount * price
                
                trade = {"order_type": order_type, "currency": currency, "amount": amount, "price": price}
        else:
            raise AttributeError("order_type is neither 'sell' nor 'buy' !")
            
        if trade:
            Account.number_of_trades = Account.number_of_trades + 1
            print("-------------- Trade Nr:" + str(Account.number_of_trades))
            print(trade)
            self.trades.append(trade)
            return trade
            
        return False
    
    def summary (self):
        print("####################")
        print("####################")
        print("########## Account Summary ##########")
        print(self.balance)
        print("### Number of Trades")
        print(len(self.trades))
        print("### Trades")
        print(self.trades)
        