# Generated by Django 5.1.1 on 2024-10-09 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0006_rename_name_order_product_order_category_order_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='category',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
    ]
