import random
from Trade import Trade

class Account():
    # 
    number_of_trades = 0
    def __init__(self, balance = {}, av_balance = None):
        """
        balance Dict
            {"btc:" 69, "euro": 12}
        av_balance FLOAT [0,1]
            =how much of the 'available balance' for each crypto currency (incl. euro) should be used for trading
        sec_balance
            secured, untouch balance =>not for trade
        """
        if balance == {}:
            raise AttributeError("No balance for currencies has been set!")
        self.balance        = balance
        self.av_balance     = av_balance
        self.sec_balance    = {}

        # (a sell closes a long and a buy closes a short)
        self.long_positions     = {} # dict of Trade() Objects
        self.short_positions    = {} # dict of Trade() Objects
        
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
    
    def execute_order(self, timestamp, order_type, currency, amount, price):
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
                
                trade = Trade(timestamp = timestamp, order_type= order_type, currency= currency, amount= amount, price= price)
                
                # add to long positions
                self.long_positions[trade.id] = trade
            
        elif order_type == "sell_short":
            # =open short position 
            # lend coins from broker and resell them right away because you expect price to fall
            if self.sufficient_balance("euro", amount*price) == True:
                self.balance["euro"]    = self.balance["euro"] - amount * price #freezing money from balance
                
                trade = Trade(timestamp = timestamp, order_type= order_type, currency= currency, amount= amount, price= price)
               
               # add to short positions
                self.short_positions[trade.id] = trade
                
        else:
            raise AttributeError("order_type is neither 'sell' nor 'buy' nor 'sell_short' nor 'buy_short' !")
            
        if trade:
            Account.number_of_trades = Account.number_of_trades + 1
            print("-------------- Trade Nr:" + str(Account.number_of_trades))
            print(trade)
            return trade
            
        return False
        
    def close_all_long_positions(self, timestamp, current_price):
        trade = None
        for pos in self.long_positions:
            if self.sufficient_balance(pos.currency, pos.amount) == True:
                self.balance[pos.currency]  = self.balance[pos.currency] - pos.amount
                self.balance["euro"]    = self.balance["euro"] + pos.amount * current_price
                
                del self.long_positions[pos.id]
                trade = Trade(timestamp = timestamp, order_type= "sell", currency= pos.currency, amount= pos.amount, price= current_price)
            else:
                raise Exception("!Trading Amount ERROR! Not enough** " + pos.currency + "** to close position")
                
        return trade
    
    def close_all_short_positions(self, timestamp, current_price):
            # =close ALL short positions 
            # buying back the lended coins and give it back to broker
            # the open position will be closed in a FIFO (First in First out) manner
        trade = None
        for pos in self.short_positions:
            p_or_l = (pos.price - current_price) * pos.amount # profit or loss
            self.balance["euro"]    = self.balance["euro"] + p_or_l
            
            del self.short_positions[pos.id]
            trade = Trade(timestamp = timestamp, order_type= "buy_short", currency= pos.currency, amount= pos.amount, price= current_price)
        
        return trade
    def check_stop_loss(self, stop_loss_val, current_price):
        """
            checks if current long or short positions need to be 
            canceled in order too loose less money
            => executes trade if necessary
            stop_loss_val Float
                % of stop_loss; E.g. if long & stop_loss_val=2% 
                    => if price already lost 2% in value position will be sold
        """
        for long_pos in self.long_positions:
            if current_price  < long_pos.price * (1 - stop_loss_val):
                print("********** Executing Stop-Loss for Long Position **********")
                #self.execute_order("sell", long_pos.currency, long_pos.amount, current_price)
                
                # remove trade from long positions
        for short_pos in self.short_positions:
            pass
            # remove trade from short positions
        
    def summary (self):
        print("####################")
        print("####################")
        print("########## Account Summary ##########")
        print("Start Budget: " + str(self.av_balance))
        print(self.balance)
        print("### Number of Trades")
        print(len(Trade.trades))
        print("### Trades")
        print(Trade.trades)
        print("### Number of open positions")
        print(len(self.short_positions))
        print("### Open positions")
        print(self.short_positions)
        
        