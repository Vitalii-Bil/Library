from rest_framework import serializers

from .models import Author, Book, Genre, Order, PublishingHouse


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio', 'date_of_birth']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']


class PublishingHouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublishingHouse
        fields = ['id', 'name', 'info', 'year']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    publishing_house = PublishingHouseSerializer(read_only=True)

    class Meta:
        many = True
        model = Book
        fields = ['id', 'title', 'year', 'price', 'description', 'publishing_house', 'author', 'genre']


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'book', 'email', 'first_name', 'last_name', 'phone', 'price', 'confirmed']
