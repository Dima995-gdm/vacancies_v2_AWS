from django.db import models


class Company(models.Model):
    name = models.CharField('Название компании', max_length=50)
    location = models.CharField('Город ', max_length=50)
    logo = models.URLField('Логотип', default='https://place-hold.it/100x60')
    description = models.CharField('Информация о компании', max_length=100)
    employee_count = models.IntegerField('Количество сотрудников')


class Specialty(models.Model):
    code = models.CharField('Код', max_length=40)
    title = models.CharField('Название специальности', max_length=50)
    picture = models.URLField('Картинка', default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    title = models.CharField('Название вакансии', max_length=50)
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.CASCADE)
    skills = models.CharField('Навыки', max_length=200)
    description = models.TextField('Описание')
    salary_min = models.IntegerField('Зарплата от')
    salary_max = models.IntegerField('Зарплата до')
    published_at = models.BooleanField('Опубликовано')






