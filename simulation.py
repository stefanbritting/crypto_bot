import datetime
import pandas as pd
class Simulation():
    # class variables
    counter = 0
    def __init__(self, start_date, end_date, df):
        """
        df [pandas dataframe]
            dataframe of the historic ohlc data
        """
        self.start_date = start_date
        self.end_date   = end_date  
        #Self.myfunc()
    
    def start(self):
        print("... starting simulation")