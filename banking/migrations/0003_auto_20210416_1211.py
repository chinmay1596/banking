# Generated by Django 3.2 on 2021-04-16 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0002_accounts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]
