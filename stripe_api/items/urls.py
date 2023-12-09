from django.urls import path

from .views import (add_item_to_order, buy_item, create_order, pay_order,
                    show_item, show_order)

urlpatterns = [
    path('buy/<int:pk>/', buy_item),
    path('item/<int:pk>/', show_item),
    path('order/create/', create_order),
    path('order/<int:pk>/', show_order),
    path('order/<int:pk>/pay/', pay_order),
    path('item/<int:pk>/add_to_order/', add_item_to_order),
]
