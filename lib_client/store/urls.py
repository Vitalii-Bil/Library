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
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:pk_cart_item>/', views.remove_from_cart, name='remove_from_cart'),
    path('genre/<int:pk>', views.genre_detail, name='genre_detail'),

    path('order/<int:pk>', views.order_detail, name='order_detail'),
    path('order/', views.OrderListView.as_view(), name='order_list'),

    path('cart-item/update/<int:pk>/', views.CartItemUpdateView.as_view(), name='cart_item_update'),
]
