# Generated by Django 2.2.17 on 2022-05-13 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211129_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Zip Code'),
        ),
    ]
