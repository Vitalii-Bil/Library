from django.urls import path

from . import views


app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
	path('book/', views.BookListView.as_view(), name='book_list'),
	path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
	path('author/', views.AuthorListView.as_view(), name='author_list'),
	path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
	path('pub-house/', views.PublishingHouseListView.as_view(), name='pub_house_list'),
	path('pub-house/<int:pk>/', views.PublishingHouseDetailView.as_view(), name='pub_house_detail'),
	path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
	path('cart/<int:pk>/', views.cart_detail, name='cart_detail')
]
