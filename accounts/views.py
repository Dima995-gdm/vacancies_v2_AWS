from django.contrib.auth.views import LoginView, LogoutView
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
        return reverse('edit_company')


class UserRegisterView(CreateView):
    """ Регистрация пользователя """
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    success_url = reverse_lazy('login_user')


class UserLogoutView(LogoutView):
    """ Выход пользователя """
    next_page = reverse_lazy('home')
