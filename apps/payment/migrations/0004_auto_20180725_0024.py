# Generated by Django 2.0.7 on 2018-07-24 15:24

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20180724_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='meta',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='amount',
            field=models.PositiveIntegerField(choices=[(1000, '1,000 원'), (3000, '3,000 원'), (5000, '5,000 원'), (10000, '10,000 원')], default=1000, verbose_name='결제 금액'),
        ),
    ]
