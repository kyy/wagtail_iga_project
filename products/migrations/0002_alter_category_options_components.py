# Generated by Django 4.1.2 on 2022-11-06 09:27

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.CreateModel(
            name='Components',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
                ('fullname', models.CharField(max_length=255, null=True, verbose_name='Полное наименование')),
                ('description', wagtail.fields.StreamField([('insert_text', wagtail.blocks.RichTextBlock(features=['h2', 'ul', 'link', 'bold', 'code'], label='Вставить текст')), ('insert_image', wagtail.images.blocks.ImageChooserBlock(label='Вставить изображение'))], blank=True, help_text='Напишите об изделии все, что считаете необходимым. Доступны: 1 блок текста; 1 изображение. ', null=True, use_json_field=True, verbose_name='Описание изделия')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'verbose_name': 'Компонент',
                'verbose_name_plural': 'Компоненты',
            },
        ),
    ]
