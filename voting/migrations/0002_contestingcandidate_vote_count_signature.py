# Generated by Django 4.2 on 2024-05-25 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestingcandidate',
            name='vote_count_signature',
            field=models.BinaryField(blank=True, default=None, null=True),
        ),
    ]
