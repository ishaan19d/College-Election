# Generated by Django 4.2 on 2024-05-24 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_pollingofficer_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollingofficer',
            name='password',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
    ]
