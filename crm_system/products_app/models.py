from django.db import models


class Product(models.Model):
    """Модель услуги"""

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Наименование услуги",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        verbose_name="Стоимость",
    )

    def __str__(self):
        return f"Услуга '{self.name}'"
