# Generated by Django 4.0.5 on 2022-06-26 14:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='status',
            field=models.CharField(default=datetime.datetime(2022, 6, 26, 14, 7, 41, 175110, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
