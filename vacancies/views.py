from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from vacancies.models import Vacancy, Company, Specialty


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        return render(request, 'vacancies/index.html', {'specialties': specialties, 'companies': companies})


class ListVacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        return render(request, 'vacancies/vacancies.html', {'vacancies': vacancies})


class SpecVacanciesView(View):
    def get(self, request):
        return HttpResponse('Вакансии по специализации')


class CardCompanyView(View):
    def get(self, request):
        vacancies_by_company = Vacancy.objects.get(company=7)
        count_vacancies = Vacancy.objects.filter(company=7).count()
        return render(request, 'vacancies/company.html', {'vacancies_by_company': vacancies_by_company,
                                                          'count_vacancies': count_vacancies,
                                                          })


class ThisVacancy(View):
    def get(self, request):
        vacancy = Vacancy.objects.get(id=2)
        return render(request, 'vacancies/vacancy.html', {'vacancy': vacancy})
