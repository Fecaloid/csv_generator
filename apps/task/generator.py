import datetime

from faker import Faker
import itertools
from config.celery import celery
from django.apps import apps
import os
from pathlib import Path
from django.conf import settings
import csv


class GeneratorSwitch:
    def __init__(self):
        self.fake = Faker()
        self.column = None

    def fake_name(self):
        return self.fake.name()

    def fake_job(self):
        return self.fake.job()

    def fake_email(self):
        return self.fake.email()

    def fake_domain(self):
        return self.fake.domain_name()

    def fake_phone(self):
        return self.fake.phone_number()

    def fake_company(self):
        return self.fake.company()

    def fake_text(self):
        return ' '.join(self.fake.sentences(self.fake.random_int(self.column.start, self.column.end)))

    def fake_int(self):
        return str(self.fake.random_int(self.column.start, self.column.end))

    def fake_address(self):
        return self.fake.address()

    def fake_date(self):
        return self.fake.date()

    def dispatch(self, column):
        method_name = 'fake_' + str(column.kind)
        self.column = column
        return getattr(self, method_name)()


@celery.task
def generate_csv(task_id):
    task_model = apps.get_model(app_label='task', model_name='Task')
    task = task_model.objects.select_related('schema').get(id=task_id)
    try:
        file_name = str(task.schema.user_id) \
            + '/' \
            + str(task.schema.id) \
            + '/'
        Path(settings.MEDIA_ROOT + file_name).mkdir(parents=True, exist_ok=True)
        file_name += str(datetime.datetime.now().strftime('%s')) + '.csv'
        with open(os.path.join(settings.MEDIA_ROOT, file_name), 'w+') as file:
            writer = csv.writer(file, delimiter=task.schema.separator)
            columns = task.schema.column_set.all()
            names = list()
            [names.append(column.name) for column in columns]
            names.insert(0, '#')
            writer.writerow(names)
            generator = GeneratorSwitch()
            counter = 1
            for _ in itertools.repeat(None, task.rows):
                item = list()
                [item.append(generator.dispatch(column)) for column in columns]
                item.insert(0, counter)
                writer.writerow(item)
                counter += 1
            task.status = 10
            task.file = file_name
            task.save()
    except Exception as e:
        task.status = 1
        task.error = e
        task.save()
        exit()
