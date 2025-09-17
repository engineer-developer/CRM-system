from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для модели клиента"""

    fields = ("name", "description", "cost")
    list_display = ("id", "name", "cost")
    list_display_links = ("name",)
    search_fields = ("name", "description")
    ordering = ("name",)
