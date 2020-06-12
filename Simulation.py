import datetime
import pandas as pd

from Strategy   import Strategy
from SimApi     import SimApi
from Account    import Account
from Trade      import Trade

class Simulation():
    # class variables
    counter = 0
    def __init__(self,start_date ,df="kraken_btcusd_1h", balance={}, av_balance = None, stake_amount = None, stop_loss = None):
        """
        start_date STRING
            e.g. 20-06-13 [format:YY-MM-DD]
        df STRING
            .csv file of the historic ohlc data place in /historic_data
        balance
        
        stake_amount FLOAT
            chunk size of a orders (e.g. always buy in packages of 50 euro)
        stop_loss FLOAT
            % threshhold for stop_loss to close order/position if going in the wrong direction
        """
        self.start_date     =  datetime.datetime.strptime(start_date, "%y-%m-%d")
        self.df             = df # for Strategy
        self.balance        = balance # for Account

        
        if stake_amount > av_balance * self.balance["euro"]:
            raise AttributeError("Stake Amount is higher than available balance for trading! Adjust either: balance, av_balance or stake_amount")
        else:
            self.av_balance     = av_balance # for Account
            self.stake_amount   = stake_amount
        
        self.stop_loss = stop_loss
        
        print("########## Configuration ##########")
        print(self.__dict__) # print configuration
        
    
    def start(self):
        print("##########... starting simulation ##########")
        self.load_historic_data()
        self.formatting_data()
        self.cut_dataframe()
        print(self.df)
        
        #api     = SimApi(self.df)
        length = len(self.df.index)
        strategy = Strategy(df = self.df, stop_loss = self.stop_loss)
        print ("########## Financial Indicators added ##########")
        
        account = Account(balance=self.balance, av_balance = self.av_balance) 
        
        start_timestamp = self.df.iloc[0].name # First entry of DF [Series.name, because the index is dtime itself]
        print ("########## starting point:")
        print(start_timestamp)
        
        # Simmulation run
        for i in range(0,length):
            
            #response = api.get_ohlc(start_timestamp + datetime.timedelta(hours=Simulation.counter)) # get ohlc from current timestamp
            
            temp_timestamp  = start_timestamp + datetime.timedelta(hours=Simulation.counter)
            price           = self.df.loc[temp_timestamp]["close"]
           
            #account.check_stop_loss()
           ############################################# 
           # if Simulation.counter == 1000 :
            #    print("break")
            ##########################################
            # buy? or close short position
            account.check_stop_loss(timestamp = temp_timestamp, stop_loss_val = self.stop_loss, current_price = price)
            
            if strategy.buy_signal(temp_timestamp):
                amount  = round(self.stake_amount / price, 15)
                account.execute_order(timestamp= temp_timestamp, order_type = "buy", currency = "btc", amount = amount, price = price )
                
                # close short
                account.close_all_short_positions(timestamp = temp_timestamp, current_price = price) 
            
            # sell? or open short position
            if strategy.sell_signal(temp_timestamp):
                account.close_all_long_positions(timestamp = temp_timestamp, current_price = price)
                
                # open short
                amount  = round(self.stake_amount / price, 15)
                account.execute_order(timestamp= temp_timestamp, order_type="sell_short", currency="btc",amount = amount, price=price)
                
            Simulation.counter = Simulation.counter  + 1
            print(Simulation.counter)
            
        print("Counter: "+ str(Simulation.counter))
        account.summary()
        
        if len(account.short_positions) > 0 or len(account.long_positions) > 0:
            # liquidate all assets at current price
            account.close_all_short_positions(timestamp = temp_timestamp, current_price = price)
            account.close_all_long_positions(timestamp = temp_timestamp, current_price = price)
            print("-------------------------------------------------")
            print("########## Account Summary with all Assets Liquidated ##########")
            account.summary()
        
        return {"account": account, "trades": Trade.trades}
        
########### Support Functions ########### 
    
    def load_historic_data(self):
        # https://www.CryptoDataDownload.com
        # loading historic data from an ohlc .csv
        
        print("### Loading csv file ...")
        csv_data = pd.read_csv("crypto_bot/historic_data/" + self.df + ".csv") #dataframe
        
        print("### Converting date column to datetime format...")
        csv_data["Date"] = pd.to_datetime(csv_data["Date"], format='%Y-%m-%d %I-%p')
        
        self.df = csv_data

    def formatting_data(self):
        # formatting & sorting data from the .csv 
        print("### Formatting data...")
        self.df = self.df.rename(columns={"Date": "dtime", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume USD": "volume"})
        self.df = self.df.drop(columns=['Symbol', 'Volume BTC'])
        self.df = self.df.set_index("dtime")
        self.df = self.df.sort_index()# order ascending
        #print(df)
        
    def cut_dataframe(self):
        # cut out rows that are before the starting date
        mask = (self.df.index >= self.start_date.strftime("%Y-%m-%d")) #boolean mask
        self.df = self.df.loc[mask]