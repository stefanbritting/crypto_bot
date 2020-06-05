import ta #https://github.com/bukosabino/ta
class Strategy():
    
    def __init__(self, df=None):
        self.df = df
        self.initialize_indicators()

    
    def buy_signal(self):
        pass
    
    def sell_signal(self):
        pass
    
    
    
    
    def initialize_indicators(self):
        # Initialize Indicator
            # Kaufmans adaptive moving average
        self.df["kama"]     = ta.momentum.KAMAIndicator(self.df["close"], n=800, pow1=20, pow2=300).kama() # first 800 rows of DF will be NaN
            
            # Accumulation/Distribution Index
        self.df["ADI"]      = ta.volume.AccDistIndexIndicator(high=self.df["high"], low=self.df["low"], close=self.df["close"], volume=self.df["volume"]).acc_dist_index()
        
        indicator_bb            = ta.volatility.BollingerBands(self.df["close"], n = 800)
        self.df["bb_high_band"] = indicator_bb.bollinger_hband()
        self.df["bb_mid_band"]  = indicator_bb.bollinger_mavg()
        self.df["bb_low_band"]  = indicator_bb.bollinger_lband()
            # ...more indicator classes
            
        # add feature to df
        
            # ...more featres
    