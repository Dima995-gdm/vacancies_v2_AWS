import os
import django


from django.http import request



os.environ['DJANGO_SETTINGS_MODULE'] = 'stepik_vacancies.settings'
django.setup()

from django.db.models import Count
from vacancies.models import Vacancy, Application

application = Application.objects.all()


print(application[0].written_username)