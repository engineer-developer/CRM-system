from django.contrib import admin

from contracts.models import Contract
from customers.models import Customer


class ContractsInline(admin.TabularInline):
    model = Contract
    fields = ["name", "cost", "is_active", "status"]
    show_change_link = True
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Админка для модели клиента"""

    readonly_fields = ("created_at", "updated_at")
    list_display = ("id", "fullname", "is_active")
    list_display_links = ("id", "fullname")
    inlines = (ContractsInline,)

    def fullname(self, obj):
        return f"{obj.lead.last_name} {obj.lead.first_name}"

    fullname.short_description = "Полное имя"
