# Generated by Django 4.1.6 on 2023-02-07 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviebbs', '0005_article_discription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='title',
        ),
    ]
