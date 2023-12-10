from django.db import models


class Item(models.Model):
    """Класс для товара"""

    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Название',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    price = models.IntegerField(
        verbose_name='Цена',
    )

    class Meta:
        """Общие параметры модели информации о товарах."""

        ordering = ('id', )
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    """Класс для корзины (заказа)"""

    item = models.ManyToManyField(
        Item,
        verbose_name='Заказ',
    )

    tax = models.ForeignKey(
        'Tax',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order',
    )

    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order',
    )

    class Meta:
        """Общие параметры модели информации о заказах."""

        ordering = ('id', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.id}'


class Discount(models.Model):
    """Класс для скидки"""

    rate = models.IntegerField(
        verbose_name='Скидка',
    )

    class Meta:
        """Общие параметры модели информации о скидках."""

        ordering = ('rate', )
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return f'Скидка {self.rate}%'


class Tax(models.Model):
    """Класс для налога"""

    rate = models.IntegerField(
        verbose_name='Налог',
    )

    class Meta:
        """Общие параметры модели информации о налогах."""

        ordering = ('rate', )
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

    def __str__(self):
        return f'Налог {self.rate}%'
