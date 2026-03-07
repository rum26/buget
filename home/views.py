from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .models import Expense
from .forms import ExpenseForm


def main(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("/")
    else:
        form = ExpenseForm()
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, "main.html", {"form": form, "expenses": expenses})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print('Вход OK!')
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            print('Ошибка входа')
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('Регистрация OK!')
            user = form.save()
            login(request, user)
            return redirect("home")
        print('Ошибка регистрации')
        print(form.errors)
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
