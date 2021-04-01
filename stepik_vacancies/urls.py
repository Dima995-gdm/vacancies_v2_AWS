from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from vacancies import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainView.as_view(), name='home'),
    path('vacancies/', views.ListVacanciesView.as_view(), name='list_all_vacancies'),
    path('vacancies/cat/<str:specialty>/', views.SpecVacanciesView.as_view(), name='vacancies_on_specialization'),
    path('companies/<int:company>/', views.CardCompanyView.as_view(), name='card_company'),
    path('vacancies/<int:vacancy>/', views.ThisVacancyView.as_view(), name='vacancy'),

    path('vacancies/<int:vacancy>/send/', views.SendRequestVacancy.as_view(), name='send_request_vacancy'),
    path('/mycompany/letsstart/', views.CreateCompanyLetsStartView.as_view(), name='create_company_lets_start'),
    path('/mycompany/create/', views.CreateCompanyView.as_view(), name='create_company'),
    path('mycompany/', views.EditCompanyView.as_view(), name='edit_company'),
    path('mycompany/vacancies/', views.ListVacanciesCompanyView.as_view(), name='list_vacancies_company'),
    path('mycompany/vacancies/create/', views.CreateVacancyCompanyView.as_view(), name='create_vacancy_company'),
    path('mycompany/vacancies/<int:vacancy>/', views.EditVacancyCompanyView.as_view(), name='edit_vacancy_company'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('register/', views.UserRegisterView.as_view(), name='register_user'),
    path('logout/', views.UserLogoutView.as_view(), name='logout_user'),

]

handler404 = views.custom_handler404
handler500 = views.custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)