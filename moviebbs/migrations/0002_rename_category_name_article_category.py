# Generated by Django 4.1.6 on 2023-02-06 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviebbs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='category_name',
            new_name='category',
        ),
    ]
