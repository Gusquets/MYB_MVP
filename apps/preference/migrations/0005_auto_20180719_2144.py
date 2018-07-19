# Generated by Django 2.0.7 on 2018-07-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preference', '0004_auto_20180719_2105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': '좋아요', 'verbose_name_plural': '좋아요'},
        ),
        migrations.AddField(
            model_name='review',
            name='like_count',
            field=models.PositiveIntegerField(default=0, verbose_name='좋아요'),
        ),
    ]