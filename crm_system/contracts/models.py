from django.db import models
from django.db.models.constraints import CheckConstraint

from customers.models import Customer
from leads.models import Lead
from products.models import Product


class Contract(models.Model):
    """Модель контракта"""

    class ContractStatus(models.TextChoices):
        """Статус контракта"""

        NEW = ("NEW", "новый")
        COMPLETED = ("COMPLETED", "исполнен")

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
        constraints = [
            CheckConstraint(
                # condition=models.Q(start_date__lt=models.F("end_date")),
                check=models.Q(start_date__lt=models.F("end_date")),
                name="check_date_constraint",
                violation_error_message="Дата начала действия контракта \
                должна быть раньше даты его окончания",
            )
        ]

    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name="Наименование",
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость контракта",
    )
    start_date = models.DateField(verbose_name="Дата начала действия контракта")
    end_date = models.DateField(verbose_name="Дата окончания действия контракта")

    product = models.ForeignKey(
        to=Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contracts",
        verbose_name="Услуга",
    )
    lead = models.ForeignKey(
        to=Lead,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contracts",
        verbose_name="Лид",
    )
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contracts",
        verbose_name="Клиент",
    )
    status = models.CharField(
        choices=ContractStatus.choices,
        default=ContractStatus.NEW,
        verbose_name="Статус",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Контракт №{self.id}"
