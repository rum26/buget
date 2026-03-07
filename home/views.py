from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .models import Expense
from .forms import ExpenseForm
from .forms import ProfileForm
from .models import Profile
from .forms import CategoryForm
from .models import Category


def main(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("/")
    else:
        form = ExpenseForm(user=request.user)
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, "main.html", {"form": form, "expenses": expenses})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print('Вход OK!')
            user = form.get_user()
            user.last_login = timezone.now()
            user.save()
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


def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)

    return render(request,
                  'edit_profile.html', {'form': form,
                                        'user': request.user})


def manage_categories(request):
    # Получаем все категории текущего пользователя
    categories = Category.objects.filter(user=request.user).order_by('name')
    # Форма для добавления новой категории
    if request.method == 'POST':
        if 'add_category' in request.POST:
            my_categories = [i.name for i in categories]
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                if category.name not in my_categories:
                    category.user = request.user
                    category.save()
                return redirect('manage_categories')
        elif 'delete_category' in request.POST:
            category_id = request.POST.get('delete_category')
            category = get_object_or_404(Category,
                                         id=category_id,
                                         user=request.user)
            category.delete()
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    return render(request, 'manage_categories.html', {
        'categories': categories,
        'form': form
    })
