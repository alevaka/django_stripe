from django.test import TestCase
from django.urls import reverse
from items.models import Item, Order


class ItemsTests(TestCase):
    def setUp(self):
        self.item0 = Item.objects.create(
            name='Test Item 0', price=11.00, currency='USD'
        )
        self.item1 = Item.objects.create(
            name='Test Item 1', price=99.00, currency='RUB'
        )
        self.item2 = Item.objects.create(
            name='Test Item 2', price=199.00, currency='RUB'
        )

    def test_show_item(self):
        """Тест показа товара"""

        response = self.client.get(reverse('show_item', args=[self.item0.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/item.html')
        self.assertEqual(response.context.get('name'), 'Test Item 0')

    def test_buy_item(self):
        """Тест покупки товара"""

        response = self.client.get(reverse('buy_item', args=[self.item0.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('session_id' in response.json())

    def test_create_order(self):
        """Тест создания заказа"""

        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('order_id' in response.json())

    def test_add_item_to_order(self):
        """Тест добавления товара в заказ"""

        order = Order.objects.create()
        response = self.client.post(
            reverse('add_item_to_order', args=[self.item0.pk]),
            {'order_id': order.id}
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse('add_item_to_order', args=[self.item1.pk]),
            {'order_id': order.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('order_items' in response.json())
        self.assertTrue('Test Item 0' in response.json()['order_items'])
        self.assertTrue('Test Item 1' in response.json()['order_items'])
        self.assertTrue('Test Item 2' not in response.json()['order_items'])

    def test_show_order(self):
        """Тест показа заказа"""

        order = Order.objects.create()
        order.item.add(self.item0)
        order.item.add(self.item1)
        response = self.client.get(reverse('show_order', args=[order.pk]))
        self.assertTemplateUsed(response, 'items/order.html')
        self.assertEqual(response.status_code, 200)

    def test_pay_order(self):
        """Тест оплаты заказа"""

        order = Order.objects.create()
        order.item.add(self.item0)
        order.item.add(self.item1)
        response = self.client.get(reverse('pay_order', args=[order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('session_id' in response.json())
