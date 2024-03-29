# Generated by Django 4.0.3 on 2022-04-15 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('exam_type', models.CharField(max_length=50)),
                ('exam_date', models.DateTimeField()),
                ('subject', models.CharField(max_length=50)),
                ('max_marks', models.IntegerField()),
                ('standard', models.IntegerField()),
                ('section', models.CharField(max_length=3)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
