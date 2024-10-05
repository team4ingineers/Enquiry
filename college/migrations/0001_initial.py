# Generated by Django 5.1.1 on 2024-10-05 23:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], max_length=50)),
                ('location', models.CharField(max_length=255)),
                ('campus_area', models.DecimalField(decimal_places=2, max_digits=6)),
                ('established_by', models.CharField(max_length=255)),
                ('nirf_ranking', models.PositiveIntegerField()),
                ('total_departments', models.PositiveIntegerField()),
                ('admission_criteria', models.CharField(max_length=255)),
                ('top_courses', models.CharField(max_length=255)),
                ('official_website', models.URLField()),
                ('image_url', models.URLField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
