import datetime
import pandas as pd

class Data():
    def __init__(self,start_date ,csv="kraken_btcusd_1h"):
        """
        start_date STRING
            e.g. 20-06-13 [format:YY-MM-DD]
        csv STRING
            .csv file of the historic ohlc data place in /historic_data
            Format: Date,Symbol,Open,High,Low,Close,Volume BTC,Volume USD
        """
        self.start_date     =  datetime.datetime.strptime(start_date, "%y-%m-%d")
        self.csv = csv
        self.df = None
        
    def load(self):        
        self.__load_historic_data()
        self.__formatting_data()
        self.__cut_dataframe()
        print(self.df)
        
        return self.df
##################### Supporting functions #####################
    def __load_historic_data(self):
        # https://www.CryptoDataDownload.com
        # loading historic data from an ohlc .csv
        
        print("### Loading csv file ...")
        csv_data = pd.read_csv("crypto_bot/historic_data/" + self.csv + ".csv") #dataframe
        
        print("### Converting date column to datetime format...")
        csv_data["Date"] = pd.to_datetime(csv_data["Date"], format='%Y-%m-%d %I-%p')
        
        self.df = csv_data

    def __formatting_data(self):
        # formatting & sorting data from the .csv 
        print("### Formatting data...")
        self.df = self.df.rename(columns={"Date": "dtime", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume USD": "volume"})
        self.df = self.df.drop(columns=['Symbol', 'Volume BTC'])
        self.df = self.df.set_index("dtime")
        self.df = self.df.sort_index()# order ascending
        #print(df)
        
    def __cut_dataframe(self):
        # cut out rows that are before the starting date
        mask = (self.df.index >= self.start_date.strftime("%Y-%m-%d")) #boolean mask
        self.df = self.df.loc[mask]