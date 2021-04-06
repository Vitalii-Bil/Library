from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, UpdateView


from .forms import CartItemForm, OrderForm
from .models import Author, Book, Cart, CartItem, Genre, Order, OrderItem, PublishingHouse
from .tasks import send_order as celery_send_order


@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.filter(book=book).exists():
        cart_item = CartItem(book=book, cart=cart)
        cart_item.save()
    messages.success(request, "Cart updated!")
    return redirect('store:book_list')


@login_required
def remove_from_cart(request, pk_cart_item):
    cart = Cart.objects.get(user=request.user)

    cart_item = CartItem.objects.get(pk=pk_cart_item, cart=cart)
    cart_item.delete()
    return redirect(reverse('store:cart_detail'))


def index(request):
    """View function for home page of site."""

    return render(request, 'store/index.html')


# @method_decorator(cache_page(60 * 60), name='dispatch')
class BookListView(ListView):
    model = Book
    paginate_by = 10
    template_name = 'store/book_list_page.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        p = Paginator(Book.objects.all().order_by('title'), self.paginate_by)
        context['articles'] = p.page(context['page_obj'].number)
        context['genre_list'] = Genre.objects.all()

        return context


# @method_decorator(cache_page(60 * 60), name='dispatch')
class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail_page.html'


# @method_decorator(cache_page(60 * 60), name='dispatch')
class PublishingHouseListView(ListView):
    model = PublishingHouse
    paginate_by = 10
    template_name = 'store/pub_house_list_page.html'


# @cache_page(60 * 60)
def pub_house_detail(request, pk):
    pub_house = get_object_or_404(PublishingHouse, pk=pk)
    books = pub_house.book_set.all().order_by('title')
    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'pub_house': pub_house,
        'page_obj': page_obj,
    }

    return render(request, 'store/pub_house_detail_page.html', context)


# @method_decorator(cache_page(60 * 60), name='dispatch')
class AuthorListView(ListView):
    model = Author
    paginate_by = 10
    template_name = 'store/author_list_page.html'


# @cache_page(60 * 60)
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.book_set.all().order_by('title')
    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'page_obj': page_obj,
    }

    return render(request, 'store/author_detail_page.html', context)


# @cache_page(60 * 60)
def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    books = genre.book_set.all().order_by('title')
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
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()

    total_cost = sum(map(lambda x: x.get_price, cart_items))

    if request.method == 'POST':

        form = OrderForm(request.POST)
        if form.is_valid():

            order = Order()
            order.email = form.cleaned_data['email']
            order.phone = form.cleaned_data['phone_number']
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.price = total_cost
            order.user = request.user
            order.save()

            books = {}

            for cart_item in cart_items:
                order_item = OrderItem()
                order_item.book_title = cart_item.book.title
                order_item.author_first_name = cart_item.book.author.first_name
                order_item.author_last_name = cart_item.book.author.last_name
                order_item.publishing_house_name = cart_item.book.publishing_house.name
                order_item.quantity = cart_item.quantity
                order_item.price = cart_item.get_price
                order_item.order = order
                order_item.save()

                books[str(cart_item.book)] = order_item.quantity
            cart.delete()
            celery_send_order.delay(order.first_name, order.last_name,
                                    order.email, order.phone, books, total_cost)

            messages.success(request, "Order created! We send you email in 10 minutes!")
            return HttpResponseRedirect(reverse('store:book_list'))
    else:
        form = OrderForm()
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
        'total_cost': round(total_cost, 2)
    }
    return render(request, 'store/cart_detail_page.html', context)


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    paginate_by = 10
    template_name = 'store/order_list_page.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('date')


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    order_items = order.orderitem_set.all()

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'store/order_detail_page.html', context)


@method_decorator(login_required, name='dispatch')
class CartItemUpdateView(UpdateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'store/cart_item_update_page.html'
    success_url = reverse_lazy('store:cart_detail')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.cart.user == request.user:
            raise Http404()
        return super().get(request, *args, **kwargs)
