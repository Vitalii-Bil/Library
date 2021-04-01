from django.contrib import admin

from .models import Author, Book, Genre, PublishingHouse


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'bio', 'date_of_birth']
    list_display = ('first_name', 'last_name')


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    fields = ['name', 'info', 'year']
    list_display = ('name', 'year')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ['title', 'year', 'publishing_house',
              'author', 'price', 'description', 'genre']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name']
