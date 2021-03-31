from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class PublishingHouse(models.Model):
    name = models.CharField(_("name"), max_length=100)
    info = models.TextField(_("info"), blank=True)
    year = models.IntegerField(_('year'))

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    bio = models.TextField(_("bio"), blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(_("name"), max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(_("title"), max_length=100)
    year = models.IntegerField(_('year'))
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)
    description = models.TextField(_("description"), blank=True)
    genre = models.ManyToManyField(Genre, verbose_name=_("genre"))
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)

    def __str__(self):
        return f'"{self.title}", {self.author}'


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', null=True, blank=True, on_delete=models.CASCADE,)
    book = models.ForeignKey(Book, verbose_name=_("book"), on_delete=models.CASCADE,)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.book}: {self.quantity}:"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    phone = models.CharField(_("phone number"), max_length=100)
    price = models.DecimalField(_('price'), max_digits=8, decimal_places=2)
    email = models.EmailField(_('email'), max_length=254)

    def __str__(self):
        return f"{self.user}'s Order"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', null=True, blank=True, on_delete=models.CASCADE,)
    book = models.ForeignKey(Book, verbose_name=_("book"), on_delete=models.CASCADE,)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book}: {self.quantity}:"
