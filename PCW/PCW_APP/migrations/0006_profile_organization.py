# Generated by Django 2.0 on 2018-03-08 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PCW_APP', '0005_remove_profile_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Organization',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
