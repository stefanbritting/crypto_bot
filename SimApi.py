import datetime

class SimApi():
    # simmulates the Kraken API during Backtesting
    def __init__(self, df=None):
        self.df = df
        
    def get_ohlc(self, timestamp=None):
        """
            timestamp [DateTime]
                time in simmulation from which data should be returned
            
            returns Pandas.DataFrame with 720 intervals (e.g. the last 720h like Kraken API)
        """

        past_timestamp   = timestamp - datetime.timedelta(hours=720)
        
        mask = (self.df.index >= past_timestamp) & (self.df.index <= timestamp)
        
        return self.df.loc[mask]