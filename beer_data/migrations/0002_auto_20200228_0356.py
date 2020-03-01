# Generated by Django 3.0.3 on 2020-02-28 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beer_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='brewery',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='geocode',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]