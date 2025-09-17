from django import forms

from contracts.models import Contract
from leads.models import Lead


class ContractForm(forms.ModelForm):
    """Форма для модели контракта"""

    lead = forms.ModelChoiceField(
        queryset=Lead.objects,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Выберите лида",
    )

    class Meta:
        model = Contract
        fields = (
            "product",
            "start_date",
            "end_date",
            "file",
        )
        widgets = {
            "product": forms.RadioSelect(),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
            ),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "product": {"required": "Необходимо выбрать хотя бы одну услугу"}
        }

    @property
    def field_order(self):
        """Задаем порядок отображения полей"""
        return ["lead", "product", "start_date", "end_date", "file"]
