# Generated by Django 4.0.5 on 2022-06-29 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_answeredquestion_examid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(max_length=2000, unique=True),
        ),
    ]
