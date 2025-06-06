# Generated by Django 5.1 on 2025-04-02 18:01

import ecom_core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_user', '0002_ecomuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecomuser',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[ecom_core.validators.validate_phone], verbose_name='Phone Number'),
        ),
    ]
