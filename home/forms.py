from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile


from .models import Expense
from .models import Category


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # форма привязана к модели Profile
        fields = ['phone', 'birth_date', 'google_table_id']
        labels = {
            'phone': 'Телефон',
            'birth_date': 'Дата рождения',
            'google_table_id': 'ID Google таблицы'
        }
        widgets = {
            'phone':forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Телефон'}),
            'birth_date': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date'}),
            'google_table_id': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'ID Google таблицы'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Категория'}),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ExpenseForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        label='Категория',
        empty_label='категория',
        widget=forms.Select(attrs={'class': 'input'}),
        required=True
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # фильтруем категории только текущего пользователя
            self.fields['category'].queryset = Category.objects.filter(
                user=user)
