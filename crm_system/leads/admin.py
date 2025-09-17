from django.contrib import admin

from leads.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Админка для модели лида"""

    readonly_fields = ("created_at", "updated_at")
    list_display = ["id", "last_name", "first_name", "phone", "is_active"]
    list_display_links = ["last_name", "first_name"]
    search_fields = ["first_name", "last_name"]
