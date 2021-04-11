import os
import django


from django.http import request



os.environ['DJANGO_SETTINGS_MODULE'] = 'stepik_vacancies.settings'
django.setup()
from django.db import models
from django.db.models import Count
from vacancies.models import Vacancy, Application, Company, Resume
from django.contrib.auth.models import User

list_users_with_companies = Resume.objects.values_list('user_id', flat=True)


print(list_users_with_companies)