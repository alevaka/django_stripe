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

    class Meta:
        """Общие параметры модели информации о заказах."""

        ordering = ('id', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.id}'
