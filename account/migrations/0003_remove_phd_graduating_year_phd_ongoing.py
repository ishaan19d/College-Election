# Generated by Django 4.2 on 2024-05-16 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_phd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phd',
            name='graduating_year',
        ),
        migrations.AddField(
            model_name='phd',
            name='ongoing',
            field=models.BooleanField(default=True),
        ),
    ]