from django.db import models
from django.contrib.auth.models import User
import quandl
import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
from scipy import stats
from django.urls import reverse
from datetime import datetime
api_key = ""

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


    #Define a way to calculate sharpe,sortino,alpha,beta of users portfolio.



################### TUTORIAL CODE I FOLLOWED ###############################
################### TUTORIAL CODE I FOLLOWED ###############################
################### TUTORIAL CODE I FOLLOWED ###############################
################### TUTORIAL CODE I FOLLOWED ###############################
################### TUTORIAL CODE I FOLLOWED ###############################
################### TUTORIAL CODE I FOLLOWED ###############################


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name




class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because a genre can contain many books and a Book can cover many genres.
    # Genre class has already been defined so we can specify the object above.

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


import uuid  # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User, User, User  # Required to assign User as a borrower


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)