from django.urls import path

from .views import (add_item_to_order, buy_item, create_order, pay_order,
                    show_item, show_order)

urlpatterns = [
    path('buy/<int:pk>/', buy_item, name='buy_item'),
    path('item/<int:pk>/', show_item, name='show_item'),
    path('order/create/', create_order, name='create_order'),
    path('order/<int:pk>/', show_order, name='show_order'),
    path('order/<int:pk>/pay/', pay_order, name='pay_order'),
    path('item/<int:pk>/add_to_order/',
         add_item_to_order, name='add_item_to_order'),
]
