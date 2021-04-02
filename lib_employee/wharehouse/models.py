from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_UPDATE, hook, LifecycleModelMixin


class PublishingHouse(models.Model):
    '''Model for publishing house with name, info and launch year'''
    name = models.CharField(_("name"), max_length=100)
    info = models.TextField(_("info"), blank=True)
    year = models.IntegerField(_('year'))

    def __str__(self):
        return self.name


class Author(models.Model):
    '''Model for author with first name, alst name, bio and date of birth'''
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    bio = models.TextField(_("bio"), blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    '''Model for genre with name fieldr'''
    name = models.CharField(_("name"), max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    '''Model for book with title, year, publishing house, author, price, description and genre'''
    title = models.CharField(_("title"), max_length=100)
    year = models.IntegerField(_('year'))
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)
    description = models.TextField(_("description"), blank=True)
    genre = models.ManyToManyField(Genre, verbose_name=_("genre"))

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    '''Model for book instance with relation to book and field sold
    (if we have on wharehouse more than 1 insctance of book)
    '''
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    sold = models.BooleanField(_('sold'), default=False)

    def __str__(self):
        return self.book.title


class Order(LifecycleModelMixin, models.Model):
    '''Order model with info about customer: email, first name, last name, phone
    and info about order: books (here we have jsonfiled with key(book titile and autor),
    value(book quantity in order))
    '''
    book = models.CharField(_("book"), max_length=100)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    phone = models.CharField(_("phone number"), max_length=100)
    price = models.DecimalField(_('price'), max_digits=8, decimal_places=2)
    confirmed = models.BooleanField(_('confirmed'), default=False)

    def __str__(self):
        return f'{self.email} order'

    @hook(AFTER_UPDATE, when='confirmed', changes_to=True)
    def send_email_after_confirmed(self):
        '''Hook: celery task, when order created for sending email to customer, that order in progress'''
        send_mail(
            subject="Your order",
            message="Your order was sent",
            from_email="ex@ex.com",
            recipient_list=[f'{self.email}'],
            fail_silently=False
        )
