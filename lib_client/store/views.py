from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Book, Author, PublishingHouse, Cart
from .forms import OrderForm


@login_required
def add_to_cart(request,pk):
    book = get_object_or_404(Book, pk=pk)
    cart,created = Cart.objects.get_or_create(user=request.user)
    messages.success(request, "Cart updated!")
    return redirect('store:book_list')


def index(request):
    """View function for home page of site."""

    return render(request, 'store/index.html')


class BookListView(ListView):
    model = Book
    paginate_by = 10
    template_name = 'store/book_list_page.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail_page.html'


class PublishingHouseListView(ListView):
    model = PublishingHouse
    paginate_by = 10
    template_name = 'store/pub_house_list_page.html'


class PublishingHouseDetailView(DetailView):
    model = PublishingHouse
    template_name = 'store/pub_house_detail_page.html'


class AuthorListView(ListView):
    model = Author
    paginate_by = 10
    template_name = 'store/author_list_page.html'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'store/author_detail_page.html'


class CartDetailView(DetailView):
    model = Cart
    template_name = 'store/cart_detail_page.html'


def cart_detail(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    books = cart.book.all()

    if request.method == 'POST':

        form = OrderForm(request.POST)

        if form.is_valid():
            
            return HttpResponseRedirect(reverse('store:book_list'))

    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart': cart,
        'books': books,
    }

    return render(request, 'store/cart_detail_page.html', context)
