# Generated by Django 3.2 on 2021-04-16 14:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0004_auto_20210416_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='account_type',
        ),
        migrations.AddField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('Savings', 'Savings'), ('Current', 'Current')], default=datetime.datetime(2021, 4, 16, 14, 13, 8, 871512, tzinfo=utc), max_length=20),
            preserve_default=False,
        ),
    ]
