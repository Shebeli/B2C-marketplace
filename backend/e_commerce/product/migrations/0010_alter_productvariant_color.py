# Generated by Django 5.1 on 2025-03-30 12:23

import ecom_core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_productvariant_color_alter_productvariant_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='color',
            field=models.CharField(blank=True, help_text="Color's Hex code", max_length=7, validators=[ecom_core.validators.validate_hex_color]),
        ),
    ]
