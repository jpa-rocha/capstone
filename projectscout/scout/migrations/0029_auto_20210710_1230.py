# Generated by Django 3.2.4 on 2021-07-10 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0028_teamstats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salarystats',
            name='estimatedtotal',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='salarystats',
            name='weeklysalary',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='salarystats',
            name='yearlysalary',
            field=models.FloatField(),
        ),
    ]
