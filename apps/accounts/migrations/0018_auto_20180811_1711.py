# Generated by Django 2.0.7 on 2018-08-11 08:11

import apps.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_artistimagestemp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artistimagestemp',
            name='image',
            field=models.ImageField(upload_to=apps.accounts.models.artist_image_upload_to_3, verbose_name='사진 1'),
        ),
    ]