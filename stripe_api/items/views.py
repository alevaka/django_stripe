from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
import stripe
from .models import Item
import os

STRIPE_API_PUBLIC_KEY = os.getenv('STRIPE_API_PUBLIC_KEY')
STRIPE_API_SECRET_KEY = os.getenv('STRIPE_API_SECRET_KEY')


def buy_item(request: HttpRequest, pk: int) -> JsonResponse:
    """Функция для покупки одного товара.
       Создаёт Stripe Session и возвращает id сессии."""

    line_items = []
    item = get_object_or_404(Item, pk=pk)
    line_items.append(
        {
          'price_data': {
            'product_data': {
              'name': item.name,
            },
            'currency': 'RUB',
            'unit_amount': item.price * 100,
          },
          'quantity': 1,
        },
    )
    stripe.api_key = STRIPE_API_SECRET_KEY
    session = stripe.checkout.Session.create(
          mode='payment',
          line_items=line_items,
          success_url=f'http://localhost:8000/api/item/{pk}/',
          cancel_url=f'http://localhost:8000/api/item/{pk}/',
      )

    json_data = {
      'pk': pk,
      'session_id': session.id,
    }
    return JsonResponse(json_data)


def show_item(request: HttpRequest, pk: int) -> HttpResponse:
    """Функция для показа страницы товара."""

    template = 'items/item.html'
    item = get_object_or_404(Item, pk=pk)
    context = {
      'pk': pk,
      'name': item.name,
      'description': item.description,
      'price': item.price,
      'STRIPE_PUBLIC_API_KEY': STRIPE_API_PUBLIC_KEY,
    }

    return render(request, template, context)
