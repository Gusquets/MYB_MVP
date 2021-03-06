# Generated by Django 2.0.7 on 2018-07-23 15:22

import apps.common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20180721_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, validators=[apps.common.validators.PhoneNumberValidator()], verbose_name='휴대폰 번호'),
        ),
    ]
