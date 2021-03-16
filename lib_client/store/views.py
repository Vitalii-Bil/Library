from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .forms import OrderForm
from .models import Author, Book, Cart, Genre, PublishingHouse


@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.book.add(book)
    messages.success(request, "Cart updated!")
    return redirect('store:book_list')


@login_required
def remove_from_cart(request, pk_book, pk_cart):
    cart = Cart.objects.get(pk=pk_cart)
    if cart.user != request.user:
        raise Http404()

    book = Book.objects.get(pk=pk_book)
    cart.book.remove(book)
    return redirect(reverse('store:cart_detail', kwargs={'pk': cart.id}))


def index(request):
    """View function for home page of site."""

    return render(request, 'store/index.html')


class BookListView(ListView):
    model = Book
    paginate_by = 10
    template_name = 'store/book_list_page.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        p = Paginator(Book.objects.all(), self.paginate_by)
        context['articles'] = p.page(context['page_obj'].number)
        context['genre_list'] = Genre.objects.all()

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail_page.html'


class PublishingHouseListView(ListView):
    model = PublishingHouse
    paginate_by = 10
    template_name = 'store/pub_house_list_page.html'


def pub_house_detail(request, pk):
    pub_house = get_object_or_404(PublishingHouse, pk=pk)
    books = Book.objects.all().filter(publishing_house=pub_house)
    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'pub_house': pub_house,
        'page_obj': page_obj,
    }

    return render(request, 'store/pub_house_detail_page.html', context)


class AuthorListView(ListView):
    model = Author
    paginate_by = 10
    template_name = 'store/author_list_page.html'


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.all().filter(author=author)
    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'page_obj': page_obj,
    }

    return render(request, 'store/author_detail_page.html', context)


def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    books = Book.objects.all().filter(genre=genre)
    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    genre_list = Genre.objects.exclude(name=genre.name)

    context = {
        'genre': genre,
        'page_obj': page_obj,
        'genre_list': genre_list
    }

    return render(request, 'store/genre_detail_page.html', context)


@login_required
def cart_detail(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    if cart.user != request.user:
        raise Http404()

    books = cart.book.all()
    total_cost = books.aggregate(Sum('price')).get('price__sum') or 0.00
    if request.method == 'POST':

        form = OrderForm(request.POST)
        if form.is_valid():
            subject = 'New order!'
            from_email = 'exx@ex.com'
            message = f"""{books} {form.cleaned_data['email']}
            {form.cleaned_data['last_name']} {form.cleaned_data['first_name']}
            {form.cleaned_data['phone_number']}"""
            send_mail(subject, message, from_email, ['admin@example.com'])

            messages.success(request, "Order created! We send you email in 10 minutes!")
            return HttpResponseRedirect(reverse('store:book_list'))
    else:
        form = OrderForm()
    context = {
        'form': form,
        'cart': cart,
        'books': books,
        'total_cost': round(total_cost, 2)
    }
    return render(request, 'store/cart_detail_page.html', context)
