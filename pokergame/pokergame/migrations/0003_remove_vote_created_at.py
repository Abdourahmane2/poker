# Generated by Django 5.0 on 2024-11-20 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokergame', '0002_vote_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='created_at',
        ),
    ]
