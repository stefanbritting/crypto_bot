from sklearn.linear_model import LinearRegression
import datetime
class CustomIndicators():
    def __init__(self, df = None):
        self.df = df

    def get_slope_acc_dist(self, i_range):
    
        x = []
        for i in range(i_range):
            x.append(i)

        x = np.array(x).reshape(-1,1)
    
        y = []
        for i in range(i_range):
            y.append(self.df.loc[self.df.iloc[0].name + datetime.timedelta(hours=i)]["acc_dist"]) # start_date + timedelta 
            
    
        y = np.array(y)
        lm = LinearRegression()
        lm.fit(x, y)
        
        plt.scatter(x, y)
        plt.plot(x,lm.predict(x), color='red')
        plt.show()
        return lm.coef_[0] # slope

start_date = datetime.datetime(2018, 6, 5)
print(df.loc[start_date]["acc_dist"])
get_slope_acc_dist(25)