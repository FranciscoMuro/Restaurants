# Generated by Django 4.0.6 on 2022-07-09 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='Phone of the restaurant'),
        ),
    ]