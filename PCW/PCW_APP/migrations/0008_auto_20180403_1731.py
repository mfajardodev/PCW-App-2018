# Generated by Django 2.0.1 on 2018-04-04 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PCW_APP', '0007_merge_20180309_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='day',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='lng',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='location',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
