from django.db import models

from leads.models import Lead


class Customer(models.Model):
    """Модель активного клиента"""

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    lead = models.OneToOneField(
        to=Lead,
        on_delete=models.PROTECT,
        related_name="customer",
        verbose_name="Лид",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    def fullname(self):
        return f"{self.lead.last_name} {self.lead.first_name}"

    def __str__(self):
        return f"Клиент '{self.fullname()}'"
