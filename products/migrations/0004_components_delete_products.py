# Generated by Django 4.1.2 on 2022-11-04 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_options_alter_products_components'),
    ]

    operations = [
        migrations.CreateModel(
            name='Components',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('description', models.TextField(max_length=1000, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Компонент',
                'verbose_name_plural': 'Компоненты',
            },
        ),
        migrations.DeleteModel(
            name='Products',
        ),
    ]
