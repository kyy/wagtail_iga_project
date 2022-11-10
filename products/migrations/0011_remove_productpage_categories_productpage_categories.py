# Generated by Django 4.1.3 on 2022-11-10 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_productpage_categories_productpage_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpage',
            name='categories',
        ),
        migrations.AddField(
            model_name='productpage',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.productcategory'),
        ),
    ]
