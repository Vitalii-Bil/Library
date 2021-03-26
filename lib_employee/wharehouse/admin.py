from django.contrib import admin

from .models import Author, Book, BookInstance, Genre, Order, PublishingHouse


def make_confirmed(modeladmin, request, queryset):
    queryset.update(confirmed=True)
make_confirmed.short_description = "Mark selected orders as confirmed"  # noqa:E305


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'bio', 'date_of_birth']
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    fields = ['name', 'info', 'year']
    list_display = ('name', 'year')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ['title', 'year', 'publishing_house',
              'author', 'price', 'description', 'genre']
    search_fields = ('title',)
    list_display = ('title', 'author')
    list_filter = ('author', 'publishing_house', 'genre')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    fields = ['book', 'sold']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['book', 'email', 'first_name', 'last_name',
              'phone', 'price', 'confirmed']
    actions = [make_confirmed]
    list_filter = ('confirmed',)
    list_display = ('email', 'phone')
    search_fields = ('email', 'phone')
