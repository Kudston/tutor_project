# Generated by Django 4.0.5 on 2022-06-26 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_examsheet_examid_remove_examsheet_examiner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examsheet',
            name='title',
        ),
    ]
