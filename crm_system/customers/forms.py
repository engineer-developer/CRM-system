from django import forms
from django.core.exceptions import ValidationError

from customers.models import Customer
from leads.models import Lead
from products.models import Product


class CustomerCreateForm(forms.Form):
    """Форма для создания клиента"""

    lead = forms.ModelChoiceField(
        queryset=Lead.objects.all(),
        required=True,
        initial=0,
        widget=forms.RadioSelect(),
        label="Выберите лида для перевода в активного клиента",
        help_text="",
    )
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=True,
        initial=0,
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


class CustomerUpdateForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ["lead"]
        widgets = {
            "lead": forms.RadioSelect(),
        }
        labels = {"lead": "Для изменения выбери лида"}
        required_fields = ["lead"]
