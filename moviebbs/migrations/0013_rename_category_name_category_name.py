# Generated by Django 4.1.7 on 2023-03-29 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviebbs', '0012_alter_comment_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_name',
            new_name='name',
        ),
    ]
