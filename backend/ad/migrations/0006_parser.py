# Generated by Django 4.0.5 on 2022-07-03 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0005_ad_created_at_ad_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]