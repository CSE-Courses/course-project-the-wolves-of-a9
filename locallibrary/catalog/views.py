from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre, Stock
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Stock.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def stock(request, tickers):
    the_stock = Stock.objects.get(ticker=str(tickers))
    has_stock = False
    user = request.user
    if user.stocks.filter(ticker=Stock.objects.get(ticker=str(tickers))).first():
        has_stock = True
    context = {
        'tick': the_stock.ticker,
        'price': the_stock.price,
        'alpha': the_stock.alpha,
        'beta': the_stock.beta,
        'sharpe': the_stock.sharpe_ratio,
        'sortino': the_stock.sortino_ratio,
        'user_has_stock': has_stock
    }

    return render(request,'stock.html', context=context)

def portfolio(request):
    returned_portfolio = []
    for x in request.user.stocks.all():
        returned_portfolio.append(str(x))
    context = {
        'portfolio': returned_portfolio,
    }
    return render(request,'portfolio.html',context=context)

def addStock(request,tickers):
    the_stock = Stock.objects.get(ticker=str(tickers))
    user = request.user
    user.stocks.create(ticker=the_stock,quantity=1)
    user.save()
    return stock(request,tickers)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})