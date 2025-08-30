from django.contrib import admin

from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Админка для модели клиента"""

    readonly_fields = ("created_at", "updated_at")
    list_display = ("id", "fullname", "is_active")
    list_display_links = ("id", "fullname")

    def fullname(self, obj):
        return f"{obj.lead.last_name} {obj.lead.first_name}"

    fullname.short_description = "Полное имя"
