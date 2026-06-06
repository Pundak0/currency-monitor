from django import forms
from .models import Currency


class CurrencyForm(forms.Form):
    """Форма для выбора валюты и периода"""
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        label="Валюта",
        empty_label="Выберите валюту",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    PERIOD_CHOICES = [
        (7, '7 дней'),
        (14, '14 дней'),
        (30, '30 дней'),
    ]

    period = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        label="Период",
        widget=forms.Select(attrs={'class': 'form-select'})
    )