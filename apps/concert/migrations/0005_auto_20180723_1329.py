# Generated by Django 2.0.7 on 2018-07-23 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concert', '0004_concertsonglist_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='probability',
            field=models.PositiveIntegerField(verbose_name='공연 확률'),
        ),
    ]
