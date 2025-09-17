from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.constraints import CheckConstraint


def upload_contract_file(instance, filename: str):
    """Указываем путь загрузки файлов"""
    return f"contracts/pdf_files/{filename}"


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
    file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        upload_to=upload_contract_file,
        null=True,
        verbose_name="Файл контракта",
    )
    start_date = models.DateField(verbose_name="Дата начала действия контракта")
    end_date = models.DateField(verbose_name="Дата окончания действия контракта")

    product = models.ForeignKey(
        to="products.Product",
        on_delete=models.SET_NULL,
        null=True,
        related_name="contracts",
        verbose_name="Услуга",
    )
    customer = models.ForeignKey(
        to="customers.Customer",
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
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        self.is_active = False
        self.save()

        if not self.customer.contracts.filter(is_active=True).exists():
            self.customer.is_active = False
            self.customer.save()

    def __str__(self):
        return f"Контракт №{self.id}"
