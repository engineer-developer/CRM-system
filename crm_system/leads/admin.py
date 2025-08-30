from django.contrib import admin

from leads.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["id", "last_name", "first_name", "phone", "created_at"]
    list_display_links = ["last_name", "first_name"]
    list_filter = ["created_at"]
    search_fields = ["first_name", "last_name"]
