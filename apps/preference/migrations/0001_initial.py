# Generated by Django 2.0.7 on 2018-07-14 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_auto_20180714_2058'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='답변')),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_artist', to='accounts.Artist', verbose_name='아티스트')),
                ('concert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_concert', to='accounts.Artist', verbose_name='공연')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='찜한 회원')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')], verbose_name='별점')),
                ('description', models.TextField(verbose_name='리뷰')),
                ('is_pay', models.BooleanField(default=False, verbose_name='후원 여부')),
                ('regist_dt', models.DateTimeField(auto_now_add=True, verbose_name='작성 시각')),
                ('like', models.PositiveIntegerField(default=0, verbose_name='좋아요')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Artist', verbose_name='아티스트')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preference.Review', verbose_name='리뷰'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자'),
        ),
    ]
