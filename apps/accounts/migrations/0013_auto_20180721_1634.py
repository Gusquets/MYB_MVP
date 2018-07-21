# Generated by Django 2.0.7 on 2018-07-21 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20180721_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='movie_1',
            field=models.URLField(blank=True, null=True, verbose_name='Youtube 영상 1'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='movie_2',
            field=models.URLField(blank=True, null=True, verbose_name='Youtube 영상 2'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='movie_3',
            field=models.URLField(blank=True, null=True, verbose_name='Youtube 영상 3'),
        ),
    ]
