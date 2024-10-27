# Generated by Django 5.0 on 2024-10-24 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fonctionnalite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=300)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='joueur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur', models.CharField(max_length=200)),
                ('fonctionnalite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokergame.fonctionnalite')),
                ('joueur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokergame.joueur')),
            ],
        ),
    ]