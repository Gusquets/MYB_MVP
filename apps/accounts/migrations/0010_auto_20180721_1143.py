# Generated by Django 2.0.7 on 2018-07-21 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_artist_rate_avg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='movie_1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Youtube 영상 1'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='movie_2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Youtube 영상 2'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='movie_3',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Youtube 영상 3'),
        ),
    ]
