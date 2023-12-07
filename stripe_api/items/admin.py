from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Отображение данных модели Item в интерфейсе администратора."""
    list_display = ('name', 'description', 'price',)
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    search_help_text = 'Поиск по названию или описанию товара'
