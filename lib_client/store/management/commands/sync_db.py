from django.core.management.base import BaseCommand
import requests

import json

from store.models import Author, Book, Genre, PublishingHouse


class Command(BaseCommand):
    help = 'Adding random users with username, email and password.'  # noqa: A003

    def handle(self, *args, **options):
        url = 'http://127.0.0.1:8000/book.json'
        response = requests.get(url).json()

        for count, book in enumerate(Book.objects.all()):
            if book.sold != response[count]['sold']:
                book.sold = response[count]['sold']

        book_counter = Book.objects.count() - 1
        if book_counter == -1: book_counter = 0
        print(book_counter)

        for resp in response[book_counter:]:

            if Author.objects.filter(bio=resp['author']['bio']).exists():
                author = Author.objects.get(bio=resp['author']['bio'])

            else:
                author = Author.objects.create(
                    first_name=resp['author']['first_name'],
                    last_name=resp['author']['last_name'],
                    bio=resp['author']['bio'],
                    date_of_birth=resp['author']['date_of_birth'],
                )

            if PublishingHouse.objects.filter(info=resp['publishing_house']['info']).exists():
                publishing_house = PublishingHouse.objects.get(info=resp['publishing_house']['info'])

            else:
                publishing_house = PublishingHouse.objects.create(
                    name=resp['publishing_house']['name'],
                    info=resp['publishing_house']['info'],
                    year=resp['publishing_house']['year'],
                )

            genre_list = []

            for genre_resp in resp['genre']:
                if Genre.objects.filter(name=genre_resp['name']).exists():
                    genre_list += [Genre.objects.get(name=genre_resp['name'])]

                else:
                    genre = Genre.objects.create(name=genre_resp['name'])
                    genre_list += [genre]

            book = Book(
                title=resp['title'],
                year=resp['year'],
                publishing_house=publishing_house,
                author=author,
                price=resp['price'],
                description=resp['description'],
                sold=resp['sold']
            )

            book.save()
            for genre in genre_list:
                book.genre.add(genre)
