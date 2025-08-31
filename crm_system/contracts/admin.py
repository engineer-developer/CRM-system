from django.contrib import admin

from contracts.models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """Админка для модели контракта"""

    readonly_fields = (
        "customer",
        "created_at",
        "updated_at",
    )
    list_display = (
        "pk",
        "name",
        "cost",
        "created_at",
    )
    list_display_links = ("name",)
    search_fields = ("name",)
