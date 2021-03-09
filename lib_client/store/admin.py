from django.contrib import admin

from .models import PublishingHouse, Author, Book, Cart


class BookInlineModelAdmin(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin, PublishingHouseAdmin)"""
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'bio', 'date_of_birth']
    inlines = [BookInlineModelAdmin]
    list_display = ('first_name', 'last_name')


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    fields = ['name', 'info', 'year']
    inlines = [BookInlineModelAdmin]
    list_display = ('name', 'year')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = ['book', 'user']
