from django.db import models
from django.db.models.constraints import CheckConstraint


class Advertisement(models.Model):
    """Модель рекламной кампании"""

    class Meta:
        verbose_name = "Рекламная кампания"
        verbose_name_plural = "Рекламные кампании"
        constraints = [
            CheckConstraint(
                check=models.Q(start_date__lt=models.F("end_date")),
                name="start_date_lt_end_date_constraint",
                violation_error_message="Дата начала должна быть меньше даты окончания",
            )
        ]

    name = models.CharField(max_length=200, null=False, verbose_name="Наименование")
    budget = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Бюджет кампании"
    )
    promotion_channel = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Канал продвижения",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="advertisements",
        verbose_name="Услуга",
    )
    start_date = models.DateField(verbose_name="Дата начала действия кампании")
    end_date = models.DateField(verbose_name="Дата окончания действия кампании")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name
