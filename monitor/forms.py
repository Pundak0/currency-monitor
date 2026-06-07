from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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


class RegisterForm(UserCreationForm):
    """Форма для регистрации нового пользователя"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})