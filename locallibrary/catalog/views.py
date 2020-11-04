from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre, Stock
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def index(request):
    """View function for home page of site."""
    # Generate list of stocks
    books = Stock.objects.all()
    # Generate counts of some of the main objects
    num_books = Stock.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    context = {
            'books': books,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def stock(request, tickers):
    the_stock = Stock.objects.get(ticker=str(tickers))
    context = {
        'tick': the_stock.ticker,
        'price': the_stock.price,
        'alpha': the_stock.alpha,
        'beta': the_stock.beta,
        'sharpe': the_stock.sharpe_ratio,
        'sortino': the_stock.sortino_ratio
    }
    return render(request,'stock.html', context=context)

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
