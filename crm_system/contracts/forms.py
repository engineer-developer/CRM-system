from django import forms

from contracts.models import Contract


class ContractForm(forms.ModelForm):
    """Форма для модели контракта"""

    class Meta:
        model = Contract
        fields = (
            "product",
            "lead",
            "start_date",
            "end_date",
        )
        widgets = {
            "product": forms.RadioSelect(),
            "lead": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
            ),
        }
        required_fields = ["product", "lead", "start_date", "end_date"]
        error_messages = {
            "product": {"required": "Необходимо выбрать хотя бы одну услугу"}
        }
