# Generated by Django 5.0 on 2024-11-20 18:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokergame', '0003_remove_vote_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]