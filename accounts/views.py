from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import request
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy

from accounts.forms import UserRegisterForm, UserLoginForm
from vacancies.models import Company


class UserLoginView(LoginView):
    """ Вход пользователя """
    model = Company
    form_class = UserLoginForm
    template_name = 'accounts/login.html'


    def get_success_url(self):
        list_users_with_companies = [id_user.owner_id for id_user in Company.objects.annotate(Count('owner_id'))]
        if self.request.user.id in list_users_with_companies:
            return reverse('edit_company')
        else:
            return reverse('create_company_lets_start')


class UserRegisterView(CreateView):
    """ Регистрация пользователя """
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    success_url = reverse_lazy('login_user')


class UserLogoutView(LogoutView):
    """ Выход пользователя """
    next_page = reverse_lazy('home')
