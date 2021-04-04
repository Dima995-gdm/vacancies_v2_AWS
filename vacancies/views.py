from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView

from vacancies.forms import ApplicationForm
from vacancies.models import Company, Specialty, Vacancy, Application


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.annotate(Count('vacancies'))
        companies = Company.objects.annotate(Count('vacancies'))
        context = {
            'specialties': specialties,
            'companies': companies,
            'request': request
        }

        return render(request, 'vacancies/index.html', context=context)


class ListVacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        return render(request, 'vacancies/vacancies.html', {'vacancies': vacancies})


class SpecVacanciesView(View):
    def get(self, request, specialty):
        specialties = get_object_or_404(Specialty, code=specialty)
        vacancies_by_specialty = Vacancy.objects.filter(specialty__code=specialty)
        context = {
            'specialty': specialty,
            'specialties': specialties,
            'vacancies_by_specialty': vacancies_by_specialty,
        }
        return render(request, 'vacancies/vacancies.html', context=context)


class CardCompanyView(View):
    def get(self, request, company):
        data_company = get_object_or_404(Company, id=company)
        vacancies_by_company = Vacancy.objects.filter(company=company)
        context = {
            'vacancies_by_company': vacancies_by_company,
            'data_company': data_company,
        }
        return render(request, 'vacancies/company.html', context=context)


class ThisVacancyView(View):

    def get(self, request, vacancy):
        this_vacancy = get_object_or_404(Vacancy, id=vacancy)
        return render(request, 'vacancies/vacancy.html', {'this_vacancy': this_vacancy, 'form': ApplicationForm})

    def post(self, request, vacancy):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.vacancy = get_object_or_404(Vacancy, id=vacancy)
            application.save()
            return redirect('send_request_vacancy')
        return render(request, 'vacancies/vacancy.html',{'form': form})




#class ThisVacancyView(DetailView, CreateView):
#    model = Vacancy
#    form_class = ApplicationForm
#    template_name = 'vacancies/vacancy.html'
#    pk_url_kwarg = 'vacancy'
#    context_object_name = 'this_vacancy'
#    success_url = reverse_lazy('send_request_vacancy')
#
#    def form_valid(self, form):
#        fields = form.save(commit=False)
#        fields.user_id = self.request.user.id
#        fields.vacancy_id = self.object.pk
#
#        form.save()





class SendRequestVacancy(View):
    """ Отправка заявки """

    def get(self, request):
        return render(request, 'vacancies/sent.html')


class CreateCompanyLetsStartView(View):
    """ Предложение создать компанию """

    def get(self, request):
        return render(request, 'vacancies/company-create.html')


class CreateCompanyView(View):
    """ Форма создания компании """

    def get(self, request):
        return render(request, 'vacancies/company-create.html')


class EditCompanyView(View):
    """ Редактирование компании """

    def get(self, request):
        return render(request, 'vacancies/company-edit.html', {'request': request})


class ListVacanciesCompanyView(View):
    """ Список вакансий у конкретной компании """

    def get(self, request):
        return render(request, 'vacancies/vacancy-list.html')


class CreateVacancyCompanyView(View):
    """ Создание вакансии у конкретной компании """

    def get(self, request):
        return render(request, 'vacancies/vacancy-edit.html')


class EditVacancyCompanyView(View):
    """ Редактирование вакансии у конкретной компании """

    def get(self, request):
        return render(request, 'vacancies/vacancy-edit.html')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Сервер не доступен!')
