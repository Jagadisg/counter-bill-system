# Generated by Django 5.0.4 on 2024-04-07 12:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_poduct_name_products_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='qauntity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
    ]
