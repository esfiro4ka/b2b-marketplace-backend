# Generated by Django 4.1 on 2023-09-03 16:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_customuser_favorite_products"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="vat",
            field=models.BooleanField(default=False),
        ),
    ]
