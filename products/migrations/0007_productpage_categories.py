# Generated by Django 4.1.3 on 2022-11-10 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpage',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productcategory'),
        ),
    ]
