from django.contrib import admin

from .models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Отображение данных модели Item в интерфейсе администратора."""
    list_display = ('name', 'description', 'price',)
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    search_help_text = 'Поиск по названию или описанию товара'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Отображение данных модели Order в интерфейсе администратора."""
    list_display = ('pk',)
    list_display_links = ('pk',)
