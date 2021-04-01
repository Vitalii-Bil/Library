from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets

from .models import Author, Book, BookInstance, Genre, Order, PublishingHouse
from .serializers import (AuthorSerializer, BookInstanceSerializer, BookInstanceSyncSerializer,
                          BookSerializer, GenreSerializer, OrderSerializer, PublishingHouseSerializer)


class BookInstanceSyncList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = BookInstance.objects.order_by('book__title', 'book__author').filter(sold=False)
    serializer_class = BookInstanceSyncSerializer
    paginator = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer


class PublishingHouseViewSet(viewsets.ModelViewSet):
    queryset = PublishingHouse.objects.all().order_by('id')
    serializer_class = PublishingHouseSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer


class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all().order_by('id')
    serializer_class = BookInstanceSerializer
