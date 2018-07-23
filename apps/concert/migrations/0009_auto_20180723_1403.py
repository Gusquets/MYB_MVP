# Generated by Django 2.0.7 on 2018-07-23 05:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concert', '0008_concert_location_else'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='probability',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='공연 확률'),
        ),
    ]
