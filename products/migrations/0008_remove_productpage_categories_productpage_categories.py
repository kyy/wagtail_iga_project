# Generated by Django 4.1.3 on 2022-11-10 11:03

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productpage_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpage',
            name='categories',
        ),
        migrations.AddField(
            model_name='productpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, null=True, to='products.productcategory'),
        ),
    ]
