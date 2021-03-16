from rest_framework import generics
from rest_framework import mixins

from .models import Book, Order
from .serializers import BookSerializer, OrderSerializer


class BookList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Book.objects.filter(sold=False).order_by('title', 'author')
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
