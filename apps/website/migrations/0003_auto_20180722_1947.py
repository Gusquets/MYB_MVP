# Generated by Django 2.0.7 on 2018-07-22 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20180722_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='terms',
            old_name='catogory',
            new_name='category',
        ),
    ]
