# Generated by Django 4.1.6 on 2023-02-14 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviebbs', '0011_alter_comment_target'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'get_latest_by': 'created_at'},
        ),
    ]
