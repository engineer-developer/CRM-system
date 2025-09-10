from django import forms
from django.core.exceptions import ValidationError

from customers.models import Customer
from leads.models import Lead, validate_phone
from products.models import Product


class CustomerCreateFromLeadForm(forms.Form):
    """Форма для создания активного клиента на основе лида"""

    product = forms.ModelChoiceField(
        queryset=Product.objects,
        required=True,
        widget=forms.RadioSelect(),
        label="Выберите услугу для клиента",
        help_text="",
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
        label="Дата начала оказания услуги",
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
        label="Дата окончания оказания услуги",
    )

    def clean(self):
        """Проверяем условие, что дата начала меньше даты окончания"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания.")

        return cleaned_data


class CustomerCreateForm(CustomerCreateFromLeadForm):
    """Форма для создания клиента"""

    lead = forms.ModelChoiceField(
        queryset=Lead.objects,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Выберите лида для перевода в активного клиента",
        help_text="",
    )
    field_order = ["lead", "product", "start_date", "end_date"]


class CustomerUpdateForm(forms.ModelForm):
    """Форма для изменения сведений об активном клиенте"""

    class Meta:
        model = Customer
        exclude = ("lead", "is_active")

    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=12,
        validators=[validate_phone],
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
