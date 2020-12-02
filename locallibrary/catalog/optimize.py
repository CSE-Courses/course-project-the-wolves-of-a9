#!/usr/bin/env python
# coding: utf-8

# In[37]:


# Programmer: Vishal R. Gangaram
# imports
import quandl
import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from scipy import stats
from scipy.optimize import minimize

get_ipython().run_line_magic('matplotlib', 'inline')
quandl.ApiConfig.api_key = "fCvBzcozBdBngMckne8C "

from jupyterthemes import jtplot
jtplot.style(theme='monokai', context='notebook', ticks=True, grid=False)


# In[8]:


start = pd.to_datetime('2000-11-03')
end = pd.to_datetime('2020-11-03')
api_key = 'fCvBzcozBdBngMckne8C '
#These are real time data sets
#AAPL_data = quandl.get("EOD/AAPL", authtoken=api_key,start_date=start, end_date=end)


# In[233]:


class PortfolioOptimizer: # Class with the capability of constructing a user poertfolio and oprtimizing it
    
    def __init__(self, dataframes=[], stock_names=[], return_df=[], close_df=[]):
        self.dataframes = dataframes # inputted dataframes from quandl
        self.stock_names = stock_names # names of the stock attributed to each dataframe in self.dataframes
        self.return_df = return_df # list of return arrays from each dataframe in self.dataframes
        self.close_df = close_df # list of close array from each dataframe in self.dataframe
        
    def add_stock(self, ticker): # Add stock method: adds stock to self.dataframe, pulls from quandl
        self.stock_names.append(ticker)
        ticker = quandl.get("eod/{stock}".format(stock = ticker), authtoken=api_key,start_date=start, end_date=end)
        self.dataframes.append(ticker)
    
    def add_holdings(self, holdings): # Adds the user's current position of each asset in within self.dataframes
        self.holdings = holdings # list that contains the user's current position in each stock within self.dataframes        

    def construct_df(self, df_lst, column): # Method that constructs a dataframe by concatinating specific arrays 
                                        # that were pulled from each dataframe in self.dataframes
        self.df_lst = df_lst
        self.column = column
        column_lst = []
        
        for i in range(len(self.df_lst)): # for loop that looks though each dataframe for the specified array
            column_lst.append(self.df_lst[i][str(self.column)]) # appends array
        stock_columns = pd.concat(column_lst, axis=1) # concatinates array
        
        if self.column == 'returns': # if the constructed df is a 'return' dataframe
            self.return_df.append(stock_columns) # append dataframe to self.return_df attribute
        elif self.column =='Close': # if the consrtucted df is a 'Close' dataframe
                self.close_df.append(stock_columns) # append dataframe to self.close_df attribute
        else: pass
        
        return stock_columns # returns constructed dataframe
    
    def get_returns(self, df1): # function that computes returns of a given stock
        self.df1 = df1
        self.df1['returns'] = self.df1['Close'].pct_change(1) # math involved in computing returns
        # doesn't return anything, instead it appends the return column to the already existing pandas df

    def get_log_returns(self): # function that computes logarithmic returns of a given stock
        log_ret = np.log(self.close_df[0] / self.close_df[0].shift(1))
        return log_ret #returns logarithmic return
    
    def calculate_ratio(self, days, ratioType): #calculates portfolio sharpe or sortino ratio of asset r_i
        spy_data = quandl.get("eod/spy", authtoken=api_key, start_date= start, end_date=end) # pings quandl
        close_df = self.close_df[0] # assigns close_df to be first index of close_df (a dataframe within an array)
        log_ret = np.log(self.close_df[0] / self.close_df[0].shift(1))
        str(ratioType).lower() # catches bad inputs, ensures if/else statement works properly
        exp_ret = np.sum((log_ret.mean() * days)) # calculates expected return 
        
        if ratioType == 'sharpe':
            exp_vol = log_ret.std() * np.sqrt(days) # calculates sharpe ratio
            sharpe_ratio = exp_ret / exp_vol
            print('The Sharpe Ratio is: {sharpe} '.format(sharpe=sharpe_ratio))
            self.sharpe_ratio = sharpe_ratio # prints sharpe ratio, assigns sharpe ratio to self.sharpe_ratio
        
        elif ratioType == 'sortino':
            exp_vol = log_ret[log_ret < 0].std() * np.sqrt(days) # same calculation, except only with downward deviation now
            sortino_ratio = exp_ret / exp_vol
            print('The Sortino Ratio is: {sortino} '.format(sortino=sortino_ratio)) # prints sortio ratio
            self.sortino_ratio = sortino_ratio
            
        else:
            pass
        
    def calculate_weights(self): # calculates the weights of portfolio from input array
        self.weights_array = self.holdings/np.sum(self.holdings) # caluclates weights
        #self.weights_array.append(i for i in weights_array)
        return self.weights_array

    def calculate_portfolio_sharpe(self, weights_array, returns_array, days): #calculates sharpe ratio of entire portfolio r_p
        exp_ret = np.sum( (returns_array.mean()  * days))
        exp_vol = returns_array.std() * np.sqrt(days)
        sharpe_ratio = exp_ret/exp_vol
        print('The Sharpe Ratio is: ')
        return sharpe_ratio # returns sharpe ratio
    
    def get_ret_vol_sr(self):
        log_ret = self.get_log_returns()
        ret = np.sum(log_ret.mean() * self.weights_array) * 252
        vol = np.sqrt(np.dot(self.weights_array.T, np.dot(log_ret.cov()*252,self.weights_array)))
        sr=ret/vol
        return np.array([ret,vol,sr])
    
    def neg_sharpe(self): return self.get_ret_vol_sr()[2] * -1
    def check_sum(self): return np.sum(self.weights_array) - 1   # return 0 if the sum of the weights is 1
    def minimize_volatility(self): return self.get_ret_vol_sr()
    
    def optimizer(self):
        cons = ({'type':'eq','fun': self.check_sum()})
        bounds = ((0,1),(0,1),(0,1),(0,1))
        init_guess = [0.25,0.25,0.25,0.25]
        opt_results = minimize(self.neg_sharpe,init_guess,method='SLSQP',bounds=bounds,constraints=cons)
        return opt_results
        
    def get_frontier_volatility(self):
        init_guess = [0.25,0.25,0.25,0.25]
        frontier_volatility = []
        for possible_return in frontier_y:
            cons = ({'type':'eq','fun':check_sum()},
                {'type':'eq','fun':lambda w: self.get_ret_vol_sr(self.weights_array)[0]-possible_return})
            result = minimize(self.minimize_volatility(),init_guess,method='SLSQP',bounds=bounds,constraints=cons)
            frontier_volatility.append(result['fun'])
        return frontier_volatility
    
    


# In[225]:


RyanPortfolio = PortfolioOptimizer()
holdings = [1,5,7,3]
RyanPortfolio.add_holdings(holdings)
RyanPortfolio.holdings

RyanPortfolio.calculate_weights()


# In[226]:


RyanPortfolio.add_stock('TSLA')
RyanPortfolio.add_stock('AAPL')
RyanPortfolio.add_stock('GOOGL')
RyanPortfolio.add_stock("SPY")


# In[227]:


for i in range(len(RyanPortfolio.dataframes)):
    RyanPortfolio.get_returns(RyanPortfolio.dataframes[i])


# In[228]:


RyanPortfolio.construct_df(RyanPortfolio.dataframes, 'returns')
RyanPortfolio.construct_df(RyanPortfolio.dataframes, 'Close')


# In[229]:


RyanPortfolio.calculate_ratio(252, 'sharpe')


# In[230]:


RyanPortfolio.return_df[0]


# In[231]:


RyanPortfolio.weights_array

