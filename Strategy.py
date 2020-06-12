import ta #https://github.com/bukosabino/ta
class Strategy():
    
    def __init__(self, df=None):
        self.df = df
        self.initialize_indicators()


    
    def buy_signal(self, timestamp):
        # multiple signals weighted
        if self.__buy_signal_1(timestamp) and self.__buy_signal_2(timestamp):
            return True
        else:
            False
    
    def sell_signal(self, timestamp):
        # multiple signals weighted
        if self.__sell_signal_1(timestamp) and self.__sell_signal_2(timestamp):
            return True
        else:
            return False
    
    
    def initialize_indicators(self):
        # Initialize Indicator
            # Kaufmans adaptive moving average
        self.df["kama"]     = ta.momentum.KAMAIndicator(self.df["close"], n=36, pow1=2, pow2=20).kama() # first 800 rows of DF will be NaN
            
            # Accumulation/Distribution Index
        self.df["ADI"]      = ta.volume.AccDistIndexIndicator(high=self.df["high"], low=self.df["low"], close=self.df["close"], volume=self.df["volume"]).acc_dist_index()
        
            # Average Directional Movement Index
        indivator_adx       = ta.trend.ADXIndicator(high=self.df["high"], low=self.df["low"], close=self.df["close"], n = 36 )
        self.df["adx_neg"]      = indivator_adx.adx_neg()
        self.df["adx_pos"]      = indivator_adx.adx_pos()
        self.df["adx"]          = indivator_adx.adx()
            # Bollinger Bands
        indicator_bb            = ta.volatility.BollingerBands(self.df["close"], n = 36)
        self.df["bb_high_band"] = indicator_bb.bollinger_hband()
        self.df["bb_mid_band"]  = indicator_bb.bollinger_mavg()
        self.df["bb_low_band"]  = indicator_bb.bollinger_lband()
        
            # ressistance line indicators
        
            # ...more featres
        print ("########## Financial Indicators added ##########")
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
    
    def __buy_signal_2(self, timestamp):
        # ADX > 22 | 25
        # +di > -di
        
        if self.df.loc[timestamp]["adx"] > 2 and self.df.loc[timestamp]["adx_pos"] > self.df.loc[timestamp]["adx_neg"] :
            return True
        else:
            return False
###############################################
    ### Sell Signals
    def __sell_signal_1(self, timestamp):
        # close price higher than middle bollinger band or kama
        if self.df.loc[timestamp]["close"] >= self.df.loc[timestamp]["bb_mid_band"]:
            return True
        else:
            return False
    
    def __sell_signal_2(self, timestamp):
        # close price higher than middle bollinger band
        if self.df.loc[timestamp]["adx_pos"] < self.df.loc[timestamp]["adx_neg"]:
            return True
        else:
            return False
        