from django.urls import path

from . import views


app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),

    path('book/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    path('author/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),

    path('pub-house/', views.PublishingHouseListView.as_view(), name='pub_house_list'),
    path('pub-house/<int:pk>/', views.pub_house_detail, name='pub_house_detail'),

    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:pk>/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:pk_book>/<int:pk_cart>', views.remove_from_cart, name='remove_from_cart'),
    path('genre/<int:pk>', views.genre_detail, name='genre_detail')
]
