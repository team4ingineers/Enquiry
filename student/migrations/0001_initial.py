# Generated by Django 5.1.1 on 2024-10-05 21:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('college', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CollegeTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='tours/')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('seen_by_college', models.BooleanField(default=False)),
                ('response', models.TextField(blank=True, null=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.college')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('abc_id', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('annual_income', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('category_certificate', models.FileField(blank=True, null=True, upload_to='category_certificates/')),
                ('disability', models.CharField(blank=True, max_length=100, null=True)),
                ('disability_certificate', models.FileField(blank=True, null=True, upload_to='disability_certificates/')),
                ('id_proof', models.FileField(blank=True, null=True, upload_to='id_proofs/')),
                ('exam_name', models.CharField(max_length=100)),
                ('exam_roll_number', models.CharField(max_length=100)),
                ('exam_marks', models.IntegerField(blank=True, null=True)),
                ('exam_certificate', models.FileField(blank=True, null=True, upload_to='exam_certificates/')),
                ('annual_income_certificate', models.FileField(blank=True, null=True, upload_to='annual_income_certificates/')),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
