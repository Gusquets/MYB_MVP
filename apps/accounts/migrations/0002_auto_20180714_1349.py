# Generated by Django 2.0.7 on 2018-07-14 04:49

import apps.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to=apps.accounts.models.artist_image_upload_to, verbose_name='사진 1'),
        ),
        migrations.AddField(
            model_name='artist',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to=apps.accounts.models.artist_image_upload_to, verbose_name='사진 2'),
        ),
        migrations.AddField(
            model_name='artist',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to=apps.accounts.models.artist_image_upload_to, verbose_name='사진 3'),
        ),
        migrations.AddField(
            model_name='artist',
            name='image_4',
            field=models.ImageField(blank=True, null=True, upload_to=apps.accounts.models.artist_image_upload_to, verbose_name='사진 4'),
        ),
        migrations.AddField(
            model_name='artist',
            name='image_5',
            field=models.ImageField(blank=True, null=True, upload_to=apps.accounts.models.artist_image_upload_to, verbose_name='사진 5'),
        ),
        migrations.AddField(
            model_name='artist',
            name='movie_1',
            field=models.URLField(blank=True, null=True, verbose_name='Youtube 영상 1'),
        ),
        migrations.AddField(
            model_name='artist',
            name='movie_2',
            field=models.URLField(blank=True, null=True, verbose_name='Youtube 영상 2'),
        ),
        migrations.AddField(
            model_name='artist',
            name='movie_3',
            field=models.URLField(blank=True, null=True, verbose_name='Youtube 영상 3'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='social_fb',
            field=models.URLField(blank=True, null=True, verbose_name='소셜_페이스북'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='social_insta',
            field=models.URLField(blank=True, null=True, verbose_name='소셜_인스타그램'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='social_youtube',
            field=models.URLField(blank=True, null=True, verbose_name='소셜_유튜브'),
        ),
    ]