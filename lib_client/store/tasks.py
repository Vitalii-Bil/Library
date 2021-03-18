from celery import shared_task
import requests

from .models import Author, Book, Genre, PublishingHouse


def change_or_add_book(resp, numb_of_similar_books):
    if Book.objects.filter(title=resp['title'], description=resp['description']).exists():
        book = Book.objects.get(title=resp['title'], description=resp['description'])
        book.quantity = numb_of_similar_books
        book.save()

    else:
        author, created = Author.objects.get_or_create(
            first_name=resp['author']['first_name'],
            last_name=resp['author']['last_name'],
            bio=resp['author']['bio'],
            date_of_birth=resp['author']['date_of_birth'],
        )

        publishing_house, created = PublishingHouse.objects.get_or_create(
            name=resp['publishing_house']['name'],
            info=resp['publishing_house']['info'],
            year=resp['publishing_house']['year'],
        )

        genre_list = []

        for genre_resp in resp['genre']:
            genre, created = Genre.objects.get_or_create(name=genre_resp['name'])
            genre_list += [genre]

        book = Book(
            title=resp['title'],
            year=resp['year'],
            publishing_house=publishing_house,
            author=author,
            price=resp['price'],
            description=resp['description'],
            quantity=numb_of_similar_books

        )

        book.save()
        for genre in genre_list:
            book.genre.add(genre)

    return


@shared_task
def sync_db():

    try:
        url = 'http://127.0.0.1:8000/book.json'
        response = requests.get(url).json()

        numb_of_similar_books = 1  # variable for counting similar books
        response_len = len(response)
        book_title_list = []  # list of book's titles, that are in api request
        book_description_list = []  # list of book's descriptions, that are in api request

        for counter, resp in enumerate(response):

            if counter != response_len - 1 and resp['title'] == response[counter + 1]['title']:
                numb_of_similar_books += 1
                continue

            else:
                change_or_add_book(resp=resp, numb_of_similar_books=numb_of_similar_books)
                numb_of_similar_books = 1
                book_title_list += [resp['title']]
                book_description_list += [resp['description']]

        sold_books = Book.objects.exclude(title__in=book_title_list,
                                          description__in=book_description_list)

        for book in sold_books:
            book.delete()

    except Exception as e:
        print('Synchronization of two databases failed. See exception:')  # noqa:T001
        print(e)  # noqa:T001
