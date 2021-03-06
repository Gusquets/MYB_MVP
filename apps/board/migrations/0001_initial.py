# Generated by Django 2.0.7 on 2018-10-20 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50, verbose_name='작성자')),
                ('content', models.CharField(max_length=200, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('login_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_login_user', to=settings.AUTH_USER_MODEL, verbose_name='회원이름')),
            ],
        ),
        migrations.CreateModel(
            name='ConcertPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50, verbose_name='작성자')),
                ('title', models.CharField(max_length=100, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('login_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='login_user', to=settings.AUTH_USER_MODEL, verbose_name='회원이름')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.ConcertPost'),
        ),
    ]
