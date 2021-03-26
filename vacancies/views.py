from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class MainView(View):
    def get(self, request):
        return render(request, 'vacancies/index.html')


class ListVacanciesView(View):
    def get(self, request):
        return render(request, 'vacancies/vacancies.html')


class SpecVacanciesView(View):
    def get(self, request):
        return HttpResponse('Вакансии по специализации')


class CardCompanyView(View):
    def get(self, request):
        return render(request, 'vacancies/company.html')


class Vacancy(View):
    def get(self, request):
        return render(request, 'vacancies/vacancy.html')
