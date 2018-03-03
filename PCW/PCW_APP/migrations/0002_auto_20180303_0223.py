# Generated by Django 2.0 on 2018-03-03 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PCW_APP', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='time',
        ),
        migrations.AddField(
            model_name='events',
            name='endTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='startTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
