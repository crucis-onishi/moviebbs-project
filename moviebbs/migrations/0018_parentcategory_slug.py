# Generated by Django 4.1.7 on 2023-05-14 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviebbs', '0017_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='parentcategory',
            name='slug',
            field=models.CharField(default='fuga', max_length=24, verbose_name='スラッグ'),
        ),
    ]
