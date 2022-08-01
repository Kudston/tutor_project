# Generated by Django 4.0.5 on 2022-06-26 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_examsheet_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='Questions',
        ),
        migrations.RemoveField(
            model_name='question',
            name='examId',
        ),
        migrations.RemoveField(
            model_name='question',
            name='questionNumber',
        ),
        migrations.AddField(
            model_name='question',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.exam'),
            preserve_default=False,
        ),
    ]
