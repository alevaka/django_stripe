from django.contrib import admin

from .models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Отображение данных модели Item в интерфейсе администратора."""
    list_display = ('name', 'description', 'price', 'currency',)
    list_display_links = ('name',)
    search_fields = ('name', 'description',)
    search_help_text = 'Поиск по названию или описанию товара'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Отображение данных модели Order в интерфейсе администратора."""
    list_display = ('pk', 'discount', 'tax',)
    list_display_links = ('pk',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Отображение данных модели Discount в интерфейсе администратора."""

    list_display = ('rate',)
    list_display_links = ('rate',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """Отображение данных модели Tax в интерфейсе администратора."""

    list_display = ('rate',)
    list_display_links = ('rate',)
