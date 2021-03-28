from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.views import View

from vacancies.models import Company, Specialty, Vacancy


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.annotate(Count('vacancies'))
        companies = Company.objects.annotate(Count('vacancies'))
        context = {
            'specialties': specialties,
            'companies': companies,
        }
        return render(request, 'vacancies/index.html', context=context)


class ListVacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        return render(request, 'vacancies/vacancies.html', {'vacancies': vacancies})


class SpecVacanciesView(View):
    def get(self, request, specialty):
        specialties = get_object_or_404(Specialty, code=specialty)
        count_vacancies_by_specialty = Vacancy.objects.filter(specialty__code=specialty).count()
        context = {
            'specialty': specialty,
            'count_vacancies_by_specialty': count_vacancies_by_specialty,
            'specialties': specialties,
        }
        return render(request, 'vacancies/vacancies.html', context=context)


class CardCompanyView(View):
    def get(self, request, company):
        vacancies_by_company = get_object_or_404(Vacancy, company=company)
        count_vacancies = Vacancy.objects.filter(company=company).count()
        context = {
            'vacancies_by_company': vacancies_by_company,
            'count_vacancies': count_vacancies,
        }
        return render(request, 'vacancies/company.html', context=context)


class ThisVacancy(View):
    def get(self, request, vacancy):
        this_vacancy = get_object_or_404(Vacancy, id=vacancy)
        return render(request, 'vacancies/vacancy.html', {'this_vacancy': this_vacancy})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Сервер не досупен!')
