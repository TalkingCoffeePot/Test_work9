# Generated by Django 5.0.1 on 2024-02-10 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='moderate',
            field=models.BooleanField(default=False, verbose_name='Модерация'),
        ),
    ]