# Generated by Django 4.0.3 on 2022-12-12 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_rename__product_orderplaced_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='_product',
            new_name='product',
        ),
    ]
