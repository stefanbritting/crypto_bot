import ta #https://github.com/bukosabino/ta
from CustomIndicators import CustomIndicators
class Strategy():
    
    def __init__(self, df=None, periods_bol = None, periods_adx = None, periods_rsi = None, adx_value = None, periods_ad = None):
        """
            periods INT
                number of periods that should be considered for indicator calculation
        """
        self.df             = df
        self.periods_bol    = periods_bol
        self.periods_adx    = periods_adx
        self.periods_rsi    = periods_rsi
        self.adx_value      = adx_value
        self.periods_ad    = periods_ad
        
        self.initialize_indicators()
        
        self.ci             = CustomIndicators(self.df)

    # ****** Note: the if functions with and are being executed in an order(left -  right)
    
    def buy_signal(self, timestamp):
        # multiple signals weighted
        if self.__buy_signal_1(timestamp) and self.__buy_signal_2(timestamp) and self.__buy_signal_3(timestamp):
            return True
        else:
            False
    
    def sell_signal(self, timestamp):
        # multiple signals weighted
        if self.__sell_signal_1(timestamp) and self.__sell_signal_2(timestamp) and self.__sell_signal_3(timestamp):
            return True
        else:
            return False
    
    
    def initialize_indicators(self):
        # Initialize Indicator
            # Kaufmans adaptive moving average
        #self.df["kama"]     = ta.momentum.KAMAIndicator(self.df["close"], n=36, pow1=2, pow2=20).kama() # first 800 rows of DF will be NaN
            
            # Accumulation/Distribution Index
        #self.df["ADI"]      = ta.volume.AccDistIndexIndicator(high=self.df["high"], low=self.df["low"], close=self.df["close"], volume=self.df["volume"]).acc_dist_index()
        
            # Average Directional Movement Index
        indivator_adx       = ta.trend.ADXIndicator(high=self.df["high"], low=self.df["low"], close=self.df["close"], n = self.periods_adx  )
        self.df["adx_neg"]      = indivator_adx.adx_neg()
        self.df["adx_pos"]      = indivator_adx.adx_pos()
        self.df["adx"]          = indivator_adx.adx()
            # Bollinger Bands
        indicator_bb            = ta.volatility.BollingerBands(self.df["close"], n = self.periods_bol )
        self.df["bb_high_band"] = indicator_bb.bollinger_hband()
        self.df["bb_mid_band"]  = indicator_bb.bollinger_mavg()
        self.df["bb_low_band"]  = indicator_bb.bollinger_lband()
        
            # RSI
        indicator_rsi   = ta.momentum.RSIIndicator(close = self.df["close"], n = self.periods_rsi )
        self.df["rsi"]  = indicator_rsi.rsi()
            
            # Accumulation / Distribution
        indicator_acc_dist  = ta.volume.AccDistIndexIndicator(high=self.df["high"], low=self.df["low"], close=self.df["close"], volume=self.df["volume"])
        self.df["acc_dist"] = indicator_acc_dist.acc_dist_index() 
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
        
        if self.df.loc[timestamp]["adx"] > self.adx_value and self.df.loc[timestamp]["adx_pos"] > self.df.loc[timestamp]["adx_neg"] :
            return True
        else:
            return False
    
    def __buy_signal_3(self, timestamp):

        
        if self.df.loc[timestamp]["rsi"] < 30:
            return True
        else:
            return False
    
    def __buy_signal_4(self, timestamp):
        # Accumulation / Distribution Indicator
        # if stock price is falling, but AD is rising => indicates strength => buy
        # https://towardsdatascience.com/linear-regression-in-6-lines-of-python-5e1d0cd05b8d
        
        slope       = self.ci.get_slope_acc_dist(timestamp =  timestamp, i_range = self.periods_ad)
        slope_close = self.ci.get_slope_closing_price(timestamp =  timestamp, i_range = self.periods_ad)
        
        if slope > 0 and slope_close < 0 :
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
    
    def __sell_signal_3(self, timestamp):
        # 
        if self.df.loc[timestamp]["rsi"] > 70:
            return True
        else:
            return False
    
    def __sell_signal_4(self, timestamp):
         # Accumulation / Distribution Indicator
        # if stock price is rising, but AD is falling => indicates weekness => sell
        pass