from django.contrib import admin

from contracts.models import Contract


@admin.action(description="Удаление контрактов без активных клиентов")
def delete_contract_with_non_client(modeladmin, request, queryset):
    """Action для удаления контрактов не имеющих активных клиентов"""
    qs = queryset.filter(customer__isnull=True)
    qs.delete()


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
        "customer",
        "is_active",
    )
    list_display_links = ("name",)
    list_filter = ("product", "is_active")
    search_fields = ("name",)
    actions = [delete_contract_with_non_client]
