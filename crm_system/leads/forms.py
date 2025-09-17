from django import forms

from leads.models import Lead


class LeadForm(forms.ModelForm):
    """Форма для модели лида"""

    class Meta:
        model = Lead
        fields = [
            "last_name",
            "first_name",
            "phone",
            "email",
            "ad",
        ]
        widgets = {
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "ad": forms.RadioSelect(),
        }
        labels = {"ad": "Через какую рекламную кампанию пришел"}
