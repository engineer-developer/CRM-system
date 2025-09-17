from django.db import models


class Customer(models.Model):
    """Модель активного клиента"""

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    lead = models.OneToOneField(
        to="leads.Lead",
        on_delete=models.PROTECT,
        related_name="customer",
        verbose_name="Лид",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def fullname(self) -> str:
        """Получаем полное имя клиента"""
        return f"{self.lead.last_name} {self.lead.first_name}"

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"Клиент '{self.fullname()}'"
