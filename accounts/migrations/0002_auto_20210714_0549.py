# Generated by Django 2.2.17 on 2021-07-14 05:49

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
    ]
