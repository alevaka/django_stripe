import os

import stripe
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Item, Order

STRIPE_API_PUBLIC_KEY = os.getenv('STRIPE_API_PUBLIC_KEY')
STRIPE_API_SECRET_KEY = os.getenv('STRIPE_API_SECRET_KEY')
HOST_ADDRESS = os.getenv('HOST_ADDRESS')

CURRENCY_SYMBOLS = {
  'USD': '$',
  'RUB': '₽',
}


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
            'currency': item.currency,
            'unit_amount': item.price * 100,
          },
          'quantity': 1,
        },
    )
    stripe.api_key = STRIPE_API_SECRET_KEY
    protocol = 'https' if request.is_secure() else 'http'
    item_url_path = reverse('show_item', args=[pk])
    item_url = f'{protocol}://{HOST_ADDRESS}{item_url_path}'
    session = stripe.checkout.Session.create(
          mode='payment',
          line_items=line_items,
          success_url=item_url,
          cancel_url=item_url,
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
      'currency': CURRENCY_SYMBOLS[item.currency],
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


def exchange_rate(currency_from: str, currency_to: str) -> int:
    """Конвертация валют.
       Для тестирования примем, что у нас только две валюты
       и курс у них стабилен."""
    rates = {
        'USD_RUB': 100,
        'RUB_USD': 0.01,
    }
    return rates.get(f'{currency_from}_{currency_to}') or 999


def show_order(request: HttpRequest, pk: int) -> JsonResponse:
    """Возвращает JSON списка товаров в заказе"""

    template = 'items/order.html'
    order = get_object_or_404(Order, pk=pk)
    items = []
    total = 0
    first_currency = None
    for item in order.item.all():
        first_currency = first_currency or item.currency
        converted_price = (item.price if first_currency == item.currency
                           else exchange_rate(item.currency, first_currency)
                           * item.price)
        total += converted_price
        items.append(item)
    discount = order.discount.rate if order.discount is not None else 0
    total_with_discount = round((total * (1 - discount/100)), 2)
    context = {
      'pk': pk,
      'items': items,
      'total': f'{total:.2f}',
      'discount': discount,
      'total_with_discount': f'{total_with_discount:.2f}',
      'first_currency': first_currency,
      'STRIPE_PUBLIC_API_KEY': STRIPE_API_PUBLIC_KEY,
      'CURRENCY_SYMBOLS': CURRENCY_SYMBOLS,
    }

    return render(request, template, context)


def pay_order(request: HttpRequest, pk: int) -> JsonResponse:
    """Оплата заказа. Создаёт Stripe Session и возвращает id сессии.
    Общая цена приводится к валюте первого товара"""

    order = get_object_or_404(Order, pk=pk)
    stripe.api_key = STRIPE_API_SECRET_KEY

    line_items = []
    tax_rate = order.tax.rate if order.tax is not None else 0
    tax = stripe.TaxRate.create(
        display_name='Налог',
        inclusive=False,
        percentage=tax_rate,
        description='Налог',
    )
    first_currency = None
    for item in order.item.all():
        first_currency = first_currency or item.currency
        converted_price = (item.price if first_currency == item.currency
                           else exchange_rate(item.currency, first_currency)
                           * item.price)
        line_items.append(
            {
              'price_data': {
                'currency': first_currency,
                'product_data': {
                  'name': item.name,
                },
                'unit_amount': int(converted_price * 100)
              },
              'quantity': 1,
              'tax_rates': [tax.id,]
            },
        )
    discounts = []
    if order.discount is not None:
        coupon = stripe.Coupon.create(
            percent_off=order.discount.rate,
            duration='once',
        )
        discounts = [{'coupon': coupon.id}]
    protocol = 'https' if request.is_secure() else 'http'
    order_url_path = reverse('show_order', args=[pk])
    order_url = f'{protocol}://{HOST_ADDRESS}{order_url_path}'
    session = stripe.checkout.Session.create(
          mode='payment',
          line_items=line_items,
          discounts=discounts,
          success_url=order_url,
          cancel_url=order_url,
      )

    json_data = {
      'pk': pk,
      'session_id': session.id
    }
    return JsonResponse(json_data)
