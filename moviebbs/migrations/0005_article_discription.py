# Generated by Django 4.1.6 on 2023-02-06 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviebbs', '0004_alter_article_movie_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='discription',
            field=models.TextField(null=True),
        ),
    ]
