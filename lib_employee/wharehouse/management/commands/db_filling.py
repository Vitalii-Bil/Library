import random

from django.core.management.base import BaseCommand
from faker import Faker
from wharehouse.models import Author, Book, BookInstance, Genre, PublishingHouse


fake = Faker()


class Command(BaseCommand):
    help = 'Generating random values for db filling'  # noqa: A003

    def handle(self, *args, **options):

        genre_list = []
        for _ in range(15):
            genre = Genre(name=fake.word())
            genre.save()
            genre_list += [genre]

        for _ in range(500):

            author = Author(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio=fake.text(max_nb_chars=400),
                date_of_birth=fake.date(),
            )
            author.save()

            publishing_house = PublishingHouse(
                name=fake.text(max_nb_chars=20),
                info=fake.text(max_nb_chars=400),
                year=random.randint(1950, 2020),
            )
            publishing_house.save()

            for _ in range(random.randint(4, 10)):
                book = Book(
                    title=fake.text(max_nb_chars=20),
                    year=random.randint(1950, 2020),
                    publishing_house=publishing_house,
                    author=author,
                    price=round(random.uniform(50, 300), 2),
                    description=fake.text(max_nb_chars=400),
                )
                book.save()

                for iterr in random.sample(range(0, 14), k=3):
                    book.genre.add(genre_list[iterr])

                for _ in range(random.randint(1, 10)):
                    book_instance = BookInstance(book=book)
                    book_instance.save()
