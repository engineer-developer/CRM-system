from django import forms

from advertisements.models import Advertisement


class AdvertisementForm(forms.ModelForm):
    """Форма для модели рекламной кампании"""

    class Meta:
        model = Advertisement
        fields = [
            "name",
            "budget",
            "product",
            "start_date",
            "end_date",
            "promotion_channel",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите наименование",
                }
            ),
            "budget": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Укажите бюджет",
                }
            ),
            "product": forms.RadioSelect(),
            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
            ),
            "promotion_channel": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Укажите канал продвижения услуги",
                }
            ),
        }
