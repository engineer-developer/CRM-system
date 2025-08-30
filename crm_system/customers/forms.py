from django import forms

from customers.models import Customer


class CustomerForm(forms.ModelForm):
    """Форма для создания модели клиента"""

    class Meta:
        model = Customer
        fields = ["lead"]
        widgets = {"lead": forms.RadioSelect}
