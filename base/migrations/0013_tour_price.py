# Generated by Django 4.0.4 on 2022-07-29 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_tour'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='price',
            field=models.DecimalField(decimal_places=15, default=299, max_digits=100),
        ),
    ]
