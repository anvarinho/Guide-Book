# Generated by Django 4.0.4 on 2022-07-29 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_tour_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='day',
            name='activities',
            field=models.ManyToManyField(blank=True, related_name='activities', to='base.activity'),
        ),
    ]
