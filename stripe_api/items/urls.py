from django.urls import path
from .views import buy_item, show_item

urlpatterns = [
    path('buy/<int:pk>/', buy_item),
    path('item/<int:pk>/', show_item),
]
