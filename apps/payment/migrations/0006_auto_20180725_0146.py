# Generated by Django 2.0.7 on 2018-07-24 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_auto_20180725_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='pay_type',
            field=models.PositiveIntegerField(choices=[(1, '카드결제'), (2, '카카오페이')], default=1, verbose_name='결제수단'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='함께 전할 메세지'),
        ),
    ]
