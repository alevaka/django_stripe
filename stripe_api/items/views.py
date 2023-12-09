import os

import stripe
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import Item, Order

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


def create_order(request: HttpRequest) -> JsonResponse:
    """Создает новый заказ и возвращает его id."""

    order = Order.objects.create()
    return JsonResponse({'order_id': order.id})


@csrf_exempt
def add_item_to_order(request: HttpRequest, pk: int) -> JsonResponse:
    """Добавляет товар в заказ.
       Номер заказа необходимо передать в строке или теле запроса."""

    order_id = request.GET.get('order_id')
    if order_id is None:
        # Если номер заказа не передан Query Parameters, ищем его в body
        order_id = request.POST.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(Item, pk=pk)
    order.item.add(item)
    items = []
    for item in order.item.all():
        items.append(str(item))
    return JsonResponse({'order_items': items})


def show_order(request: HttpRequest, pk: int) -> JsonResponse:
    """Возвращает JSON списка товаров в заказе"""

    # order = get_object_or_404(Order, pk=pk)
    # items = []
    # for item in order.item.all():
    #     items.append(str(item))
    # return JsonResponse({'order_items': items})
    template = 'items/order.html'
    order = get_object_or_404(Order, pk=pk)
    items = []
    total = 0
    for item in order.item.all():
        total += item.price
        items.append(item)
    context = {
      'pk': pk,
      'items': items,
      'total': total,
      'STRIPE_PUBLIC_API_KEY': STRIPE_API_PUBLIC_KEY,
    }

    return render(request, template, context)


def pay_order(request: HttpRequest, pk: int) -> JsonResponse:
    """Оплата заказа. Создаёт Stripe Session и возвращает id сессии"""

    order = get_object_or_404(Order, pk=pk)
    line_items = []
    for item in order.item.all():
        line_items.append(
            {
              'price_data': {
                'currency': 'RUB',
                'product_data': {
                  'name': item.name,
                },
                'unit_amount': int(item.price * 100)
              },
              'quantity': 1,
            },
        )
    stripe.api_key = STRIPE_API_SECRET_KEY
    session = stripe.checkout.Session.create(
          mode='payment',
          line_items=line_items,
          success_url=f'http://localhost:8000/api/order/{pk}/',
          cancel_url=f'http://localhost:8000/api/order/{pk}/'
      )

    json_data = {
      'pk': pk,
      'session_id': session.id
    }
    return JsonResponse(json_data)
