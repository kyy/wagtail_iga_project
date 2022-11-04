# Generated by Django 4.1.2 on 2022-11-04 10:37

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_components_delete_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='components',
            name='body',
            field=wagtail.fields.StreamField([('txt_block', wagtail.blocks.RichTextBlock())], blank=True, null=True, use_json_field=True, verbose_name='Описание изделия'),
        ),
        migrations.AlterField(
            model_name='components',
            name='description',
            field=models.TextField(max_length=1000, null=True, verbose_name='Описание'),
        ),
    ]