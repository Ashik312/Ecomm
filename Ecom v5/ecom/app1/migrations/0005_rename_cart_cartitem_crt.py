# Generated by Django 4.2.5 on 2023-10-03 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_remove_cart_pro_remove_cart_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='cart',
            new_name='crt',
        ),
    ]
