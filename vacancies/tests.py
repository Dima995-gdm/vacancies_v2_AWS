from django.test import TestCase

from stepik_vacancies.data import companies

for i in companies:
    for l,m in i.items():
        print(l,m)
