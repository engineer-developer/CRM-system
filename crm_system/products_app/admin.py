from django.contrib import admin

from products_app.models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "cost")
    list_display_links = ("name",)
    ordering = ("name",)
