# Generated by Django 2.0.7 on 2018-07-24 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_auto_20180725_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='amount',
            field=models.PositiveIntegerField(choices=[(1000, '1,000 원'), (3000, '3,000 원'), (5000, '5,000 원'), (10000, '10,000 원')], default=3000, verbose_name='결제 금액'),
        ),
    ]
