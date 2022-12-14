# Generated by Django 4.0.5 on 2022-06-19 05:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examId', models.CharField(default=uuid.uuid4, max_length=225)),
                ('title', models.CharField(max_length=2000)),
                ('dateCreated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='examRegistrationLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examId', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examId', models.CharField(max_length=255)),
                ('questionId', models.CharField(default=uuid.uuid4, max_length=255)),
                ('questionNumber', models.IntegerField()),
                ('question', models.CharField(max_length=2000)),
                ('option_a', models.CharField(max_length=2000)),
                ('option_b', models.CharField(max_length=2000)),
                ('option_c', models.CharField(blank=True, max_length=2000)),
                ('option_d', models.CharField(blank=True, max_length=2000)),
                ('option_e', models.CharField(blank=True, max_length=2000)),
                ('option_f', models.CharField(blank=True, max_length=2000)),
                ('answer', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='userProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userImage', models.ImageField(default='default.jpeg', upload_to='usersPics')),
                ('is_student', models.BooleanField(default=False)),
                ('is_tutor', models.BooleanField(default=False)),
                ('dateJoined', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutorId', models.CharField(blank=True, default=uuid.uuid4, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='examSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examSheetId', models.CharField(default=uuid.uuid4, max_length=225)),
                ('examId', models.CharField(max_length=225)),
                ('title', models.CharField(max_length=2000)),
                ('dateRegistered', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_answered', models.BooleanField(default=False)),
                ('examiner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.tutor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='examRequestObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examId', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='examRecordSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalQuestions', models.IntegerField(null=True)),
                ('score', models.IntegerField(null=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='Questions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.question'),
        ),
        migrations.AddField(
            model_name='exam',
            name='examSheets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.examsheet'),
        ),
        migrations.AddField(
            model_name='exam',
            name='examiner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.tutor'),
        ),
        migrations.CreateModel(
            name='answeredQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examId', models.CharField(max_length=255)),
                ('questionId', models.CharField(max_length=255)),
                ('questionNumber', models.IntegerField()),
                ('answer', models.CharField(max_length=2000)),
                ('correct', models.BooleanField(default=False)),
                ('wrong', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
