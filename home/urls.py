from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name='home'),
    path("login/", views.login_view, name='login'),
    path("register/", views.registration, name='register')

]
