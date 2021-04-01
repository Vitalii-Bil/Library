from rest_framework import serializers

from .models import Author, Book, BookInstance, Genre, Order, PublishingHouse


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['url', 'id', 'first_name', 'last_name', 'bio', 'date_of_birth']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['url', 'id', 'name']


class PublishingHouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublishingHouse
        fields = ['url', 'id', 'name', 'info', 'year']


class BookSyncSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    publishing_house = PublishingHouseSerializer(read_only=True)

    class Meta:
        many = True
        model = Book
        fields = ['id', 'title', 'year', 'price', 'description',
                  'publishing_house', 'author', 'genre']


class BookInstanceSyncSerializer(serializers.ModelSerializer):
    book = BookSyncSerializer(read_only=True)

    class Meta:
        many = True
        model = BookInstance
        fields = ['id', 'book', 'sold']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        many = True
        model = Book
        fields = ['id', 'title', 'year', 'price', 'description',
                  'publishing_house', 'author', 'genre']


class BookInstanceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        many = True
        model = BookInstance
        fields = ['id', 'book', 'sold']


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'book', 'email', 'first_name',
                  'last_name', 'phone', 'price', 'confirmed']
