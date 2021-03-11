from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# Create a router and register our viewsets with it.

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('book/', views.BookList.as_view()),
    path('order/create', views.OrderCreate.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
