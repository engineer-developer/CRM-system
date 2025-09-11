from django.contrib import admin

from advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """Админка для рекламной кампании"""

    list_display = [
        "name",
        "budget",
        "promotion_channel",
    ]
