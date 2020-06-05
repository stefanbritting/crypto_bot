import ta #https://github.com/bukosabino/ta
class Strategy():
    
    def __init__(self, df=None):
        self.df = df
        self.initialize_indicators()

    
    def buy_signal(self, timestamp):
        # multiple signals weighted
        return self.__buy_signal_1(timestamp)
    
    def sell_signal(self, timestamp):
        # multiple signals weighted
        return self.__sell_signal_1(timestamp)
    
    
    
    
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
        
            # ...more featres
    ########## Signals ##########
    # each signal holds a set of rules that analyce current financial situation
    # if value is NaN => False
    ### Buy Signals
    def __buy_signal_1(self, timestamp):
        # close hit lower bollinger band
        
        if self.df.loc[timestamp]["close"] <= self.df.loc[timestamp]["bb_low_band"]:
            return True
        else:
            return False
    
    ### Sell Signals
    def __sell_signal_1(self, timestamp):
        if self.df.loc[timestamp]["close"] >= self.df.loc[timestamp]["bb_high_band"]:
            return True
        else:
            return False
        