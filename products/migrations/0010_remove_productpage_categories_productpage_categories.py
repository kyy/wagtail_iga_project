# Generated by Django 4.1.3 on 2022-11-10 11:28

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_productpage_categories_productpage_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpage',
            name='categories',
        ),
        migrations.AddField(
            model_name='productpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='products.productcategory'),
        ),
    ]
