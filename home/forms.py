from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Expense


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ExpenseForm(forms.ModelForm):
    category = forms.CharField(
            required=False,
            label="",
            widget=forms.TextInput(attrs={
                "placeholder": "Категория",
                "class": "input"
            })
        )

    title = forms.CharField(
            required=False,
            label="",
            widget=forms.TextInput(attrs={
                "placeholder": "Название",
                "class": "input"
            })
        )

    amount = forms.DecimalField(
            label="",
            widget=forms.NumberInput(attrs={
                "placeholder": "Сумма",
                "class": "input",
                "min": "0"
            })
        )

    class Meta:
        model = Expense
        fields = ["category", "title", "amount"]
