from django.db import models
from django.contrib.auth.models import User
from phonenumber_field import modelfields

from stepik_vacancies.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    specialty = models.ForeignKey('Specialty', related_name="vacancies", on_delete=models.CASCADE)
    company = models.ForeignKey('Company', related_name="vacancies", on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

    def __str__(self):
        return f'{self.pk} {self.title}'


class Company(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.CharField(max_length=100)
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, related_name='owner_of_company', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.pk} {self.name}'


class Specialty(models.Model):
    code = models.CharField(max_length=40)
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return f'{self.pk} {self.title}'


class Application(models.Model):
    written_username = models.CharField(max_length=100, unique=True)
    written_phone = modelfields.PhoneNumberField(unique=True)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} {self.written_username}'









