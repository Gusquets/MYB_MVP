# Generated by Django 2.0.7 on 2018-07-22 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preference', '0005_auto_20180719_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.IntegerField(choices=[(0, '☆☆☆☆☆'), (1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=0, verbose_name='별점'),
        ),
    ]