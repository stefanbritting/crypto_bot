import datetime
import pandas as pd
from Strategy import Strategy
class Simulation():
    # class variables
    counter = 0
    def __init__(self,start_date=None,end_date=None,df="kraken_btcusd_1h"):
        """
        df STRING
            .csv file of the historic ohlc data place in /historic_data
        """
        self.start_date = start_date
        self.end_date   = end_date
        self.df         = df
        
    
    def start(self):
        print("... starting simulation")
        data = self.load_historic_data()
        data = Simulation.formatting_data(data)
        strat = Strategy(data)
    
    def load_historic_data(self):
        # https://www.CryptoDataDownload.com
        print("### Loading csv file ...")
        csv_data = pd.read_csv("crypto_bot/historic_data/" + self.df + ".csv") #dataframe
        
        print("### Converting date column to datetime format...")
        csv_data["Date"] = pd.to_datetime(csv_data["Date"], format='%Y-%m-%d %I-%p')
        
        return csv_data

    @staticmethod
    def formatting_data(df=None):
        print("### Formatting data...")
        df = df.rename(columns={"Date": "dtime", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume USD": "volume"})
        df = df.drop(columns=['Symbol', 'Volume BTC'])
        df = df.set_index("dtime")
        df = df.sort_index()# order ascending
        #print(df)
        
        return df