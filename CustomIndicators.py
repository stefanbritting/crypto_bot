from sklearn.linear_model import LinearRegression
import numpy as np
import datetime
class CustomIndicators():
    def __init__(self, df = None):
        self.df = df

    def get_slope_acc_dist(self,timestamp ,i_range):
        """
            periods INT
                number of periods that should be considered for indicator calculation
        """
    
        x = []
        for i in range(i_range):
            x.append(i)

        x = np.array(x).reshape(-1,1)
    
        y = []
        for i in range(i_range):
            y.append(self.df.loc[timestamp - datetime.timedelta(hours=i)]["acc_dist"]) # start_date - timedelta => to he past
            
    
        y = np.array(y)
        lm = LinearRegression()
        lm.fit(x, y)
        

        return lm.coef_[0] # slope
        
    def get_slope_closing_price(self,timestamp ,i_range):
        """
            periods INT
                number of periods that should be considered for indicator calculation
        """
    
        x = []
        for i in range(i_range):
            x.append(i)

        x = np.array(x).reshape(-1,1)
    
        y = []
        for i in range(i_range):
            y.append(self.df.loc[timestamp - datetime.timedelta(hours=i)]["close"]) # start_date - timedelta => to he past
            
    
        y = np.array(y)
        lm = LinearRegression()
        lm.fit(x, y)
        

        return lm.coef_[0] # slope

