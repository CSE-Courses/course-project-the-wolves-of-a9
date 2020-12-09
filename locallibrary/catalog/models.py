from django.db import models
from django.contrib.auth.models import User
import quandl
import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
from scipy import stats
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
import datetime
from secret.protected import quandl_key
api_key = quandl_key

class StockHistory(models.Model):
    ticker = models.CharField(max_length=5, unique=False)
    open_price = models.DecimalField(max_digits=20,decimal_places=10,null=True)
    close_price = models.DecimalField(max_digits=20,decimal_places=10,null=True)
    high_price = models.DecimalField(max_digits=20,decimal_places=10,null=True)
    low_price = models.DecimalField(max_digits=20,decimal_places=10,null=True)
    adj_close = models.DecimalField(max_digits=20,decimal_places=10,null=True)
    volume = models.DecimalField(max_digits=20,decimal_places=2,null=True)

    timestamp = models.DateTimeField(auto_now_add=False)

class Stock(models.Model):
    ticker = models.CharField(max_length=5,unique=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    sharpe_ratio = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    sortino_ratio = models.DecimalField(max_digits=8, decimal_places=5, null=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    alpha = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    beta = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    #updater = StockManager()

    def __str__(self):
        return self.ticker

    # Creates a column called 'get_returns' that consists of the percent changes of the closing products for each stock.
    def get_returns(self, df1):
        df1['returns'] = df1['Close'].pct_change(1)
        return df1['returns']  # Returns one column.

    def get_log_returns(self,close_df, column):
        log_ret = np.log(close_df[column] / close_df[column].shift(1))
        return log_ret

    def construct_df(self,df_lst, column):
        column_lst = []
        for i in range(len(df_lst)):
            column_lst.append(df_lst[i][str(column)])
        stock_columns = pd.concat(column_lst, axis=1)
        return stock_columns

    def update_alpha_and_beta(self):
        spy_data = quandl.get("eod/spy", authtoken=api_key,start_date="2019-10-19",end_date="2020-10-19")
        stock_data = quandl.get("eod/{stock}".format(stock=str(self.ticker)), authtoken=api_key,start_date="2019-10-19",end_date="2020-10-19")
        spy_returns = self.get_returns(spy_data)
        stock_returns = self.get_returns(stock_data)
        if len(stock_data['Open']) != 252:
            print("Error: {Stock} is incomplete. Length of stock_data['Open'] is {number}".format(Stock=self.ticker, number = len(stock_data['Open'])))
            return
        self.beta, self.alpha, r_value, p_value, std_err = stats.linregress(
            stock_returns.iloc[1:], spy_returns.iloc[1:])
        self.price = stock_data['Close'][-1]
        #self.date_updated = datetime.now()
        self.save()
        print("Alpha and Beta successfully updated! {Stock}:, Alpha: {alpha}, Beta: {beta}, Price: {price}".format(Stock=str(self.ticker),alpha=self.alpha,beta=self.beta, price= stock_data['Close'][-1]))

    def calculate_ratio(self, days, ratioType):
        stock_data = quandl.get("eod/{stock}".format(stock=str(self.ticker)), authtoken=api_key,
                                start_date="2019-10-19", end_date="2020-10-19")
        spy_data = quandl.get("eod/spy", authtoken=api_key, start_date="2019-10-19", end_date="2020-10-19")
        close_df = stock_data["Close"]
        log_ret = np.log(close_df / close_df.shift(1))
        str(ratioType).lower()
        exp_ret = np.sum((log_ret.mean() * days))
        if ratioType == 'sharpe':
            exp_vol = log_ret.std() * np.sqrt(days)
            sharpe_ratio = exp_ret / exp_vol
            print('The Sharpe Ratio is: {sharpe} '.format(sharpe=sharpe_ratio))
            self.sharpe_ratio = sharpe_ratio
            self.save()
        elif ratioType == 'sortino':
            exp_vol = log_ret[log_ret < 0].std() * np.sqrt(days)
            sortino_ratio = exp_ret / exp_vol
            print('The Sortino Ratio is: {sortino} '.format(sortino=sortino_ratio))
            self.sortino_ratio = sortino_ratio
            self.save()
        else:
            pass

    def get_history(self, period = 'day') :
        end_date = timezone.now()
        start_date = end_date - timedelta(days=1)

        if period == 'week' :
            start_date = end_date - timedelta(days=7)
        if period == 'month' :
            start_date = end_date - timedelta(days=30)
        if period == 'year' :
            start_date = end_date - timedelta(days=365)

        history = StockHistory.objects.filter(ticker=self.ticker).filter(timestamp__range=(start_date, end_date)).order_by('timestamp')

        return list(map(lambda x : {
                "date":x.timestamp.isoformat().split('T')[0],
                "open_price": float(x.open_price),
                "close_price":float(x.close_price),
                "high_price":float(x.high_price),
                "low_price":float(x.low_price),
                "adj_close":float(x.adj_close)
            }, history))

class UserStockOwnership(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE)
    sharpe_ratio = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    sortino_ratio = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    alpha = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    beta = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="stocks")

    def __str__(self):
        return "{ticker}: {quantitys}".format(ticker=self.ticker.ticker,quantitys=self.quantity)
