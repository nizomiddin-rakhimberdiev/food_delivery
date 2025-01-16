# Generated by Django 5.1.4 on 2025-01-16 04:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_restaurant_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="restaurant",
            name="address",
        ),
        migrations.CreateModel(
            name="RestaurantBranch",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("address", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="branches",
                        to="core.restaurant",
                    ),
                ),
            ],
        ),
    ]
