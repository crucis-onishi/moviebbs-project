# Generated by Django 4.1.7 on 2023-05-14 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviebbs', '0016_article_movie_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(default='hoge', max_length=24, verbose_name='スラッグ'),
        ),
    ]
