from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView

from vacancies.forms import ApplicationForm, CompanyForm, VacancyForm, ResumeForm
from vacancies.models import Company, Specialty, Vacancy, Application, Resume


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.annotate(Count('vacancies'))
        companies = Company.objects.annotate(Count('vacancies'))
        context = {
            'specialties': specialties,
            'companies': companies,
            'request': request,
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
        this_vacancy = get_object_or_404(Vacancy, id=vacancy)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.vacancy = get_object_or_404(Vacancy, id=vacancy)
            application.save()
            return redirect('send_request_vacancy', vacancy)
        return render(request, 'vacancies/vacancy.html', {'form': form, 'this_vacancy': this_vacancy})


class SendRequestVacancy(View):
    """ Отправка заявки """

    def get(self, request, vacancy):
        return render(request, 'vacancies/sent.html', {'vacancy': vacancy})


class CreateCompanyLetsStartView(View):
    """ Предложение создать компанию """

    def get(self, request):
        if request.user.id in Company.objects.values_list('owner_id', flat=True):
            return redirect('edit_company')

        return render(request, 'vacancies/company-create.html')


class CreateCompanyView(View):
    """ Форма создания компании """

    def get(self, request):
        if request.user.id not in Company.objects.values_list('owner_id', flat=True):
            return redirect('create_company_lets_start')

        return render(request, 'vacancies/company-edit.html', {'form': CompanyForm})

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, 'Кампания успешно создана!')
            return redirect('edit_company')
        messages.error(request, 'Вы ввели неверные данные!')
        return render(request, 'vacancies/vacancy.html', {'form': form})


class EditCompanyView(SuccessMessageMixin, UpdateView):
    """ Редактирование компании """

    model = Company
    template_name = 'vacancies/company-edit.html'
    success_url = reverse_lazy('edit_company')
    form_class = CompanyForm
    success_message = 'Информация о компании обновлена!'

    def get_object(self, queryset=None):
        return self.request.user.owner_of_company

    def get(self, request, *args, **kwargs):
        try:
            form = CompanyForm(instance=self.get_object())
            return render(request, 'vacancies/company-edit.html', {'form': form})

        except ObjectDoesNotExist:
            return redirect('create_company_lets_start')


class ListVacanciesCompanyView(View):
    """ Список вакансий у конкретной компании """

    def get(self, request):
        vacancies_by_company = Vacancy.objects.filter(company__owner_id=self.request.user)
        return render(request, 'vacancies/vacancy-list.html', {'vacancies_by_company': vacancies_by_company})


class CreateVacancyCompanyView(View):
    """ Создание вакансии у конкретной компании """

    def get(self, request):
        return render(request, 'vacancies/vacancy-edit.html', {'form': VacancyForm})

    def post(self, request):
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company_id = Company.objects.get(owner_id=self.request.user).pk
            vacancy.save()
            return redirect('list_vacancies_company')
        messages.error(request, 'Вы ввели неверные данные!')
        return render(request, 'vacancies/vacancy.html', {'form': form})


class EditVacancyCompanyView(SuccessMessageMixin, UpdateView):
    """ Редактирование вакансии у конкретной компании """

    model = Vacancy
    template_name = 'vacancies/vacancy-edit.html'
    form_class = VacancyForm
    pk_url_kwarg = 'vacancy'
    success_message = 'Вакансия успешно обновлена!'

    def get_context_data(self, **kwargs):
        context = super(EditVacancyCompanyView, self).get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(vacancy=self.object)
        return context


class SearchView(ListView):
    """ Поиск вакансии по названию или описанию """
    template_name = 'vacancies/search.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacancy.objects.filter(
            Q(title__icontains=self.request.GET.get('s')) | Q(description__icontains=self.request.GET.get('s')),
        )


class CreateResumeLetsStartView(View):
    """ Предложение создать резюме """

    def get(self, request):
        if request.user.id in Resume.objects.values_list('user_id', flat=True):
            return redirect('edit_resume')

        return render(request, 'vacancies/resume-create.html')


class CreateResume(SuccessMessageMixin, View):
    """ Создание резюме """

    def get(self, request):
        if request.user.id not in Resume.objects.values_list('user_id', flat=True):
            return redirect('create_resume_lets_start')
        return render(request, 'vacancies/resume-edit.html', {'form': ResumeForm})

    def post(self, request):
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, 'Резюме успешно создано!')
            return redirect('edit_resume')
        messages.error(request, 'Вы ввели неверные данные!')
        return render(request, 'vacancies/vacancy.html', {'form': form})


class EditResume(SuccessMessageMixin, UpdateView):
    """ Редактирование резюме """

    model = Resume
    template_name = 'vacancies/resume-edit.html'
    success_url = reverse_lazy('edit_resume')
    form_class = ResumeForm
    success_message = 'Информация о вашем резюме обновлена!'

    def get_object(self, queryset=None):
        return self.request.user.resume

    def get(self, request, *args, **kwargs):
        try:
            form = ResumeForm(instance=self.get_object())
            return render(request, 'vacancies/resume-edit.html', {'form': form})

        except ObjectDoesNotExist:
            return redirect('create_resume_lets_start')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def custom_handler500(request):
    return HttpResponseServerError('Сервер не доступен!')
