# Generated by Django 2.0 on 2018-03-03 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PCW_APP', '0002_auto_20180303_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='QR_code',
            field=models.URLField(null=True),
        ),
    ]
