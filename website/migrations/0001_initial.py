# Generated by Django 3.2 on 2021-04-22 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dp', models.ImageField(default='/dp.jpg', upload_to='photo/')),
                ('phone', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('gender', models.CharField(blank=True, default='', max_length=10, null=True)),
                ('about', models.TextField(blank=True, default='', null=True)),
                ('clinic_name', models.CharField(blank=True, max_length=256, null=True)),
                ('price', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('Specialization', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('mark', models.BooleanField(default=False)),
                ('degree', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('degree_name', models.CharField(default='Doctor', max_length=30)),
                ('services', models.CharField(default='', max_length=256)),
                ('state', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Zoom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('access_token', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('token_type', models.CharField(default='', max_length=1000)),
                ('refresh_token', models.CharField(default='', max_length=1000)),
                ('expires', models.DateTimeField()),
                ('scope', models.CharField(default='', max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hospital', models.CharField(max_length=256)),
                ('post', models.CharField(default='', max_length=256)),
                ('start', models.CharField(max_length=256)),
                ('end', models.CharField(max_length=256)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_first_login', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('slot', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('startUrl', models.URLField(default='https://google.com', max_length=256)),
                ('meetUrl', models.URLField(default='https://google.com', max_length=256)),
                ('docId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.doctordetails')),
                ('patientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatientDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.CharField(default='', max_length=256)),
                ('country', models.CharField(default='', max_length=256)),
                ('phone', models.CharField(default='', max_length=256)),
                ('dp', models.ImageField(blank=True, default='dp.jpg', null=True, upload_to='patients/photos/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('userD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.userdetails')),
            ],
        ),
        migrations.CreateModel(
            name='allPatients',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.patientdetails')),
            ],
        ),
    ]