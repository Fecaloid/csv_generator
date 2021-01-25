from faker import Faker
from apps.task.models import Task
import itertools


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

    def fake_date(self):
        return self.fake.date()

    def dispatch(self, column):
        method_name = 'fake_' + str(column.kind)
        self.column = column
        return getattr(self, method_name)()


def generate_csv(task_id):
    task = Task.objects.select_related('schema').get(id=task_id)
    print(task)
    print(task.schema)
    columns = task.schema.column_set.all()
    names = list()
    [names.append(column.name) for column in columns]
    print(names)
    generator = GeneratorSwitch()
    data = list()
    for _ in itertools.repeat(None, task.rows):
        item = list()
        [item.append(generator.dispatch(column)) for column in columns]
        data.append(item)
    print(data)
