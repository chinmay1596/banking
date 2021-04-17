# Generated by Django 3.2 on 2021-04-16 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('Savings', 'Savings'), ('Current', 'Current')], max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default='0.00', max_digits=9)),
                ('account_no', models.PositiveBigIntegerField()),
                ('Transcation_type', models.CharField(choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdraw'), ('Enquiry', 'Enquiry')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]