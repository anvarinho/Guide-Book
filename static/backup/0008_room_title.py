# Generated by Django 4.0.4 on 2022-07-19 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_room_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
