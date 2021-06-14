# Generated by Django 3.2.4 on 2021-06-11 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0005_playingtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralStats',
            fields=[
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='scout.player')),
                ('goals', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('nonPKgoals', models.IntegerField()),
                ('PKgoals', models.IntegerField()),
                ('attemptedPK', models.IntegerField()),
                ('yellowcards', models.IntegerField()),
                ('redcards', models.IntegerField()),
            ],
        ),
    ]
