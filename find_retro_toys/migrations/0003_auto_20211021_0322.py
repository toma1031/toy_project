# Generated by Django 2.2.17 on 2021-10-21 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_retro_toys', '0002_auto_20211005_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(upload_to='images/photo_from_user', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to='images/photo_from_user', verbose_name='Photo2'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo3',
            field=models.ImageField(blank=True, null=True, upload_to='images/photo_from_user', verbose_name='Photo3'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo4',
            field=models.ImageField(blank=True, null=True, upload_to='images/photo_from_user', verbose_name='Photo4'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo5',
            field=models.ImageField(blank=True, null=True, upload_to='images/photo_from_user', verbose_name='Photo5'),
        ),
    ]
