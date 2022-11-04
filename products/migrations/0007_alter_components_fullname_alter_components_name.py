# Generated by Django 4.1.2 on 2022-11-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_components_body_components_fullname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='components',
            name='fullname',
            field=models.CharField(max_length=255, null=True, verbose_name='Полное наименование'),
        ),
        migrations.AlterField(
            model_name='components',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Наименование'),
        ),
    ]