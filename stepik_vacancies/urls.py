"""stepik_vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('vacancies/<int:vacancy>/', views.ThisVacancy.as_view(), name='vacancy'),

]

handler404 = views.custom_handler404
handler500 = views.custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)