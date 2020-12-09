import quandl
import os

from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import make_aware

from catalog.models import Stock, StockHistory
from secret.protected import quandl_key

quandl.ApiConfig.api_key = quandl_key

def updateStockData():
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)

    start_date = start_date.isoformat().split('T')[0]
    end_date = end_date.isoformat().split('T')[0]


    for stock in Stock.objects.all():
        print(stock.ticker)
        data = quandl.get(
            "eod/{stock}".format(stock=str(stock.ticker)),
            start_date=start_date,
            end_date=end_date
        )
        for row in data.iterrows():
            row[0].isoformat().split('T')[0]
            try :
                try:
                    entry = StockHistory.objects.get(ticker=stock.ticker, timestamp=row[0])
                    entry.open_price = row[1]["Open"]
                    entry.close_price = row[1]["Close"]
                    entry.high_price = row[1]["High"]
                    entry.low_price = row[1]["Low"]
                    entry.adj_close = row[1]["Adj_Close"]
                    entry.volume = row[1]["Volume"]
                    entry.save()
                except StockHistory.DoesNotExist:
                    StockHistory( ticker = stock.ticker, open_price = row[1]["Open"], close_price = row[1]["Close"], high_price = row[1]["High"], low_price = row[1]["Low"], adj_close = row[1]["Adj_Close"], volume = row[1]["Volume"],timestamp = make_aware(row[0])).save()
                except Exception as e:
                    print(e)
            except Exception as e :
                print(e)
            if row[0].isoformat().split('T')[0] == end_date:
                try:
                    stock.price = row[1]["Close"]
                    stock.date_updated = make_aware(row[0])
                    stock.save()
                except Exception as e:
                    print(e)

    return

def addStock(ticker):
    ticker = ticker.upper()
    end_date = timezone.now()
    end_date = end_date - timedelta(days=1)
    start_date = end_date - timedelta(days=365)

    start_date = start_date.isoformat().split('T')[0]
    end_date = end_date.isoformat().split('T')[0]

    if Stock.objects.filter(ticker=ticker).exists():
        print(entry)
    else:
        try:
            data = quandl.get(
                "eod/{stock}".format(stock=str(ticker)),
                start_date=start_date,
                end_date=end_date
                )
        except Exception as e:
            print(e)
            return
        for row in data.iterrows():
            try :
                StockHistory( ticker = ticker, open_price = row[1]["Open"], close_price = row[1]["Close"], high_price = row[1]["High"], low_price = row[1]["Low"], adj_close = row[1]["Adj_Close"], volume = row[1]["Volume"],timestamp = make_aware(row[0])).save()
            except Exception as e :
                print(e)
            if row[0].isoformat().split('T')[0] == end_date:
                try:
                    Stock(ticker = ticker, price = row[1]["Close"], date_updated = make_aware(row[0])).save()
                except Exception as e:
                    print(e)
    return
