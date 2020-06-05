import datetime
import pandas as pd
from Strategy import Strategy
from SimApi import SimApi

class Simulation():
    # class variables
    counter = 0
    def __init__(self,start_date ,df="kraken_btcusd_1h"):
        """
        start_date STRING
            e.g. 20-06-13 [format:YY-MM-DD]
        df STRING
            .csv file of the historic ohlc data place in /historic_data
        """
        self.start_date =  datetime.datetime.strptime(start_date, "%y-%m-%d")
        self.df         = df
        
    
    def start(self):
        print("... starting simulation")
        self.load_historic_data()
        self.formatting_data()
        self.cut_dataframe()
        print(self.df)
        
        #api     = SimApi(self.df)
        length = len(self.df.index)
        strategy = Strategy(self.df)
        start_timestamp = self.df.iloc[0].name # First entry of DF [Series.name, because the index is dtime itself]
        print ("### starting point:")
        print(start_timestamp)
        
        # Simmulation run
        for i in range(0,length):
            
            #response = api.get_ohlc(start_timestamp + datetime.timedelta(hours=Simulation.counter)) # get ohlc from current timestamp
            
            # add indicators to response => Strategy class
            
            # buy?
                
            # sell?
            
            
            Simulation.counter = Simulation.counter  + 1
            print(Simulation.counter)
            
        print("Counter: "+ str(Simulation.counter))
        
########### Support Functions ########### 
    
    def load_historic_data(self):
        # https://www.CryptoDataDownload.com
        print("### Loading csv file ...")
        csv_data = pd.read_csv("crypto_bot/historic_data/" + self.df + ".csv") #dataframe
        
        print("### Converting date column to datetime format...")
        csv_data["Date"] = pd.to_datetime(csv_data["Date"], format='%Y-%m-%d %I-%p')
        
        self.df = csv_data

    def formatting_data(self):
        print("### Formatting data...")
        self.df = self.df.rename(columns={"Date": "dtime", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume USD": "volume"})
        self.df = self.df.drop(columns=['Symbol', 'Volume BTC'])
        self.df = self.df.set_index("dtime")
        self.df = self.df.sort_index()# order ascending
        #print(df)
        
    def cut_dataframe(self):
        mask = (self.df.index >= self.start_date.strftime("%Y-%m-%d")) #boolean mask
        self.df = self.df.loc[mask]