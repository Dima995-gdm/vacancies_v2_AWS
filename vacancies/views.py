from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class MainView(View):
    def get(self, request):
        return HttpResponse('Главная страница')


class ListVacanciesView(View):
    def get(self, request):
        return HttpResponse('Список вакансий')


class SpecVacanciesView(View):
    def get(self, request):
        return HttpResponse('Вакансии по специализации')


class CardCompanyView(View):
    def get(self, request):
        return HttpResponse('Карточка компании')


class Vacancy(View):
    def get(self, request):
        return HttpResponse('Вакансия')
