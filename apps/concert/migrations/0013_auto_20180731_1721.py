# Generated by Django 2.0.7 on 2018-07-31 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concert', '0012_auto_20180731_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='rain_cancel',
            field=models.BooleanField(choices=[(True, '네'), (False, '아니오')], default=False, verbose_name='우천시 취소여부'),
        ),
        migrations.AlterField(
            model_name='concert',
            name='site_reserved',
            field=models.BooleanField(choices=[(True, '네'), (False, '아니오')], default=False, verbose_name='장소 예약여부'),
        ),
    ]
