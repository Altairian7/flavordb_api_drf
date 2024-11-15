# Generated by Django 5.1.3 on 2024-11-15 13:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Compound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compound_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('taste_profile', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='HealthySwap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_ingredient', models.CharField(max_length=200)),
                ('healthy_alternative', models.CharField(max_length=200)),
                ('nutritional_difference', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('recipe', models.TextField()),
                ('nutritional_info', models.JSONField()),
                ('ingredients', models.JSONField()),
                ('weather_suitable', models.CharField(blank=True, max_length=100)),
                ('season_suitable', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BeveragePairing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beverage', models.CharField(max_length=200)),
                ('pairing_notes', models.TextField()),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_records', models.TextField(blank=True)),
                ('allergies', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorite', models.BooleanField(default=False)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TasteProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compound_preferences', models.JSONField()),
                ('taste_vector', models.JSONField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='meals.userprofile')),
            ],
        ),
    ]
