# Generated by Django 4.0.4 on 2022-07-31 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_activity_day_activities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='rooms',
        ),
        migrations.AddField(
            model_name='tour',
            name='rooms',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='base.room'),
        ),
    ]
