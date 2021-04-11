from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from phonenumber_field import modelfields
from django.utils import timezone

from stepik_vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Vacancy(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название вакансии')
    specialty = models.ForeignKey('Specialty', related_name="vacancies", on_delete=models.CASCADE,
                                  verbose_name='Специализация')
    company = models.ForeignKey('Company', related_name="vacancies", on_delete=models.CASCADE)
    skills = models.CharField(max_length=200, verbose_name='Требуемые навыки')
    description = models.TextField(verbose_name='Описание вакансии')
    salary_min = models.IntegerField(verbose_name='Зарплата от')
    salary_max = models.IntegerField(verbose_name='Зарплата до')
    published_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.pk} {self.title}'

    def get_absolute_url(self):
        return reverse('edit_vacancy_company', kwargs={'vacancy': self.pk})


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название компании')
    location = models.CharField(max_length=50, verbose_name='География')
    logo = models.ImageField(
        upload_to=MEDIA_COMPANY_IMAGE_DIR,
        verbose_name='Логотип', blank=True, default='company_images/default.png',
        )
    description = models.CharField(max_length=100, verbose_name='Информация о компании')
    employee_count = models.IntegerField(verbose_name='Количество человек в компании')
    owner = models.OneToOneField(User, on_delete=models.PROTECT, related_name='owner_of_company')

    def __str__(self):
        return f'{self.pk} {self.name}'


class Specialty(models.Model):
    code = models.CharField(max_length=40)
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return f'{self.title}'


class Application(models.Model):
    written_username = models.CharField(max_length=100, verbose_name='Имя')
    written_phone = modelfields.PhoneNumberField(region='RU', unique=True, verbose_name='Телефон')
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} {self.written_username}'


class Resume(models.Model):
    class Status(models.TextChoices):
        NOT_LOOKING = ('NOT_LOOKING', 'Не ищу работу')
        CONSIDER = ('CONSIDER', 'Рассматриваю предложения')
        LOOKING = ('LOOKING', 'Ищу работу')

    class Grade(models.TextChoices):
        TRAINEE = ('TRAINEE', 'Стажер')
        JUNIOR = ('JUNIOR', 'Джуниор')
        MIDDLE = ('MIDDLE', 'Миддл')
        SENIOR = ('SENIOR', 'Сеньор')
        LID = ('LID', 'Лид')

    user = models.OneToOneField(User, related_name='resume', on_delete=models.PROTECT)
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    status = models.CharField(choices=Status.choices, max_length=24, verbose_name='Готовность к работе')
    salary = models.IntegerField(verbose_name='Ожидаемое вознаграждение')
    specialty = models.ForeignKey('Specialty', related_name="resume", on_delete=models.CASCADE,
                                  verbose_name='Специализация')
    grade = models.CharField(choices=Grade.choices, max_length=24, verbose_name='Квалификация')
    education = models.TextField(verbose_name='Образование')
    experience = models.TextField(verbose_name='Опыт работы')
    portfolio = models.URLField(verbose_name='Ссылка на партфолио')

    def __str__(self):
        return f'{self.pk} {self.user}'
