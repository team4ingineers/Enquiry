# Generated by Django 5.1.1 on 2024-10-06 01:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0001_initial'),
        ('student', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_score', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('number_of_agreements', models.PositiveIntegerField(default=0)),
                ('number_of_disagreements', models.PositiveIntegerField(default=0)),
                ('college', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='college.college')),
            ],
        ),
        migrations.CreateModel(
            name='StudentFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_type', models.CharField(choices=[('Agree', 'Agree'), ('Disagree', 'Disagree')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('college_health_score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.healthscore')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
