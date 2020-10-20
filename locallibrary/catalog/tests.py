from django.test import TestCase
from .models import *
from django.contrib.auth.models import User


class StockTestCase(TestCase):
    def setUp(self):
        Stock.objects.create(ticker="AAPL")
        Stock.objects.create(ticker="ETSY")
        User.objects.create(username="tester")

    def test_Stock(self):
        aapl = Stock.objects.get(ticker="AAPL")
        user = User.objects.get(username="tester")
        user.stocks.create(ticker=Stock.objects.get(ticker="AAPL"),quantity=5)

        self.assertEqual(aapl,user.stocks.first().ticker)
        self.assertEqual(5, user.stocks.first().quantity)
        self.assertEqual(aapl, Stock.objects.get(ticker="AAPL"))
        aapl.update_alpha_and_beta()
        self.assertEqual(aapl.price, 115.98)

    def test_Portfolio(self):
        user = User.objects.get(username="tester")
        aapl = Stock.objects.get(ticker="AAPL")

        user.stocks.create(ticker=Stock.objects.get(ticker="AAPL"), quantity=5)
        user.stocks.create(ticker=Stock.objects.get(ticker="ETSY"), quantity=3)

        self.assertEqual(aapl, user.stocks.first().ticker)
        self.assertEqual(2, user.stocks.all().count())