# Generated by Django 4.0.5 on 2022-06-29 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_exam_questions_remove_question_examid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answeredquestion',
            name='examId',
        ),
        migrations.RemoveField(
            model_name='answeredquestion',
            name='questionId',
        ),
        migrations.RemoveField(
            model_name='answeredquestion',
            name='questionNumber',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='examSheets',
        ),
        migrations.AddField(
            model_name='answeredquestion',
            name='exam',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.exam'),
            preserve_default=False,
        ),
    ]
