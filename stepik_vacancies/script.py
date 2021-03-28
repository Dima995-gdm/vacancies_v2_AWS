import os
import django

from stepik_vacancies.data import jobs, companies, specialties
from vacancies.models import Vacancy, Company, Specialty

os.environ['DJANGO_SETTINGS_MODULE'] = 'stepik_vacancies.settings'
django.setup()

if __name__ == '__main__':
    for data_specialties in specialties:
        Specialty.objects.create(
            code=data_specialties.get('code'),
            title=data_specialties.get('title'),
        )

    for data_companies in companies:
        Company.objects.create(
            name=data_companies.get('title'),
            location=data_companies.get('location'),
            description=data_companies.get('description'),
            employee_count=data_companies.get('employee_count'),
        )

    for data_jobs in jobs:
        Vacancy.objects.create(
            title=data_jobs.get('title'),
            specialty=Specialty.objects.get(code=data_jobs.get('specialty')),
            company=Company.objects.get(id=data_jobs.get('company')),
            skills=data_jobs.get('skills'),
            description=data_jobs.get('description'),
            salary_min=data_jobs.get('salary_from'),
            salary_max=data_jobs.get('salary_to'),
            published_at=data_jobs.get('posted'),
        )
