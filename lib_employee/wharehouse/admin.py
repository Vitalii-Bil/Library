from django.contrib import admin
from django.core.mail import send_mail

from .models import Author, Book, BookInstance, Genre, Order, PublishingHouse
#  from .tasks import order_ready_send_mail as celery_order_ready_send_mail


def make_confirmed(modeladmin, request, queryset):
    '''Action for making selected orders as confirmed'''
    queryset.update(confirmed=True)
    for q_obj in queryset:
        #  celery_order_ready_send_mail.delay(q_obj.email)
        send_mail(
            subject="Your order",
            message="Your order was sent.",
            from_email="ex@ex.com",
            recipient_list=[f'{q_obj.email}'],
            fail_silently=False
        )
make_confirmed.short_description = "Mark selected orders as confirmed"  # noqa:E305


def make_sold(modeladmin, request, queryset):
    '''Action for making selected books as sold'''
    queryset.update(sold=True)
make_sold.short_description = "Mark selected books as sold"  # noqa:E305


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    '''Author ModelAdmin for displaying all data and searching by fields'''
    fields = ['first_name', 'last_name', 'bio', 'date_of_birth']
    list_display = ('first_name', 'last_name', 'date_of_birth')
    search_fields = ('first_name', 'last_name')


@admin.register(PublishingHouse)
class PublishingHouseAdmin(admin.ModelAdmin):
    '''PublishingHouse ModelAdmin for displaying all data and searching by fields'''
    fields = ['name', 'info', 'year']
    list_display = ('name', 'year')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    '''Book ModelAdmin for displaying all data, searching by fields and filtering'''
    fields = ['title', 'year', 'publishing_house',
              'author', 'price', 'description', 'genre']
    search_fields = ('title',)
    list_display = ('title', 'author', 'year')
    list_filter = ('author', 'publishing_house', 'genre')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    '''Genre ModelAdmin for displaying all data'''
    fields = ['name']


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    '''BookInstance ModelAdmin for displaying all data, searching by fields and action'''
    fields = ['book', 'sold']
    search_fields = ('book__title',)
    actions = [make_sold]
    list_filter = ('book',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Order ModelAdmin for displaying all data, searching by fields and action'''
    fields = ['book', 'email', 'first_name', 'last_name',
              'phone', 'price', 'confirmed']
    actions = [make_confirmed]
    list_filter = ('confirmed',)
    list_display = ('email', 'phone')
    search_fields = ('email', 'phone')
