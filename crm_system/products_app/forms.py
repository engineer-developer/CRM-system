from django import forms

from products_app.models import Product


class ProductForm(forms.ModelForm):
    """форма для услуги"""

    class Meta:
        model = Product
        fields = ["name", "description", "cost"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                }
            ),
            "cost": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Наименование услуги",
            "description": "Описание услуги",
            "cost": "Стоимость услуги",
        }
