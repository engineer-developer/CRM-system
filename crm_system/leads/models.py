from django.db import models
from django.core.exceptions import ValidationError


def validate_phone(value: str):
    if not value.startswith(("+7", "8")):
        raise ValidationError("Phone number must be entered in the format: +7 or 8")
    if not value[1:].isdigit():
        raise ValidationError("Phone number must contain only digits")


class Lead(models.Model):
    """Модель лида"""

    class Meta:
        verbose_name = "Лид"
        verbose_name_plural = "Лиды"

    last_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Фамилия",
    )
    first_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Имя",
    )
    phone = models.CharField(
        unique=True,
        max_length=12,
        null=False,
        verbose_name="Телефон",
        validators=[validate_phone],
    )
    email = models.EmailField(
        max_length=120,
        null=False,
        blank=True,
        verbose_name="Email",
    )
    is_active = models.BooleanField(default=True, null=False, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        self.is_active = False
        self.save()

    def fullname(self):
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"Лид '{self.fullname()}'"
