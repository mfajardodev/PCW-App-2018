# Generated by Django 2.0.3 on 2018-04-06 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PCW_APP', '0009_auto_20180403_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='hostee',
            field=models.BooleanField(default=False),
        ),
    ]