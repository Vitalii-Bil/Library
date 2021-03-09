from django.conf import settings
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
        return f"{self.last_name}, {self.first_name}"


class Book(models.Model):
    title = models.CharField(_("title"), max_length=100)
    year = models.IntegerField(_('year'))
    publishing_house = models.ForeignKey(PublishingHouse, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)
    description = models.TextField(_("description"), blank=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    book = models.ManyToManyField(Book, verbose_name=_("book"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s cart"
