# Generated by Django 3.1.5 on 2021-01-26 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_auto_20210126_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='separator',
            field=models.CharField(choices=[(',', ','), (';', ';'), ('|', '|'), (':', ':')], default=';', max_length=1, verbose_name='Separator'),
        ),
    ]