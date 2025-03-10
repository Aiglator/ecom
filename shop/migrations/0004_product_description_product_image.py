# Generated by Django 5.1.3 on 2025-01-21 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_product_description_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
