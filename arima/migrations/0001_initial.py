# Generated by Django 2.1.15 on 2020-02-06 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arima',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('output', models.CharField(max_length=200)),
                ('total_time', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(max_length=200, null=True)),
                ('log_file', models.CharField(max_length=200, null=True)),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('resolved_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
