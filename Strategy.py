import ta
class Strategy():
    
    def __init__(self, df=None):
        self.df = Strategy.initialize_indicators(df)
        print(df)
    
    def buy_signal(self):
        pass
    
    def sell_signal(self):
        pass
    
    
    
    @staticmethod
    def initialize_indicators(df=None):
        # Initialize Indicator
        kama = ta.momentum.KAMAIndicator(df["close"], n=720)
            # ...more indicator classes
            
        # add feature to df
        df["kama"] = kama.kama()
            # ...more featres
        return df
    