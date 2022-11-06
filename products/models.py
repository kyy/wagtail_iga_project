from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.formats import Format, register_image_format



@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория продукции'
        verbose_name_plural = 'Категории продукции'

@register_snippet
class Components(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=50, null=False, blank=False,  unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    fullname = models.CharField(verbose_name='Полное наименование', max_length=255, null=True, blank=False)
    description = StreamField([
        ('insert_text', RichTextBlock(
            features=['h2', 'ul', 'link', 'bold', 'code'],
            label='Вставить текст',
        )),
        ('insert_image', ImageChooserBlock(
            label='Вставить изображение',
        )),
    ],
        block_counts={
            'insert_text': {'max_num': 1},
            'insert_image': {'max_num': 1},
        },
        use_json_field=True,
        verbose_name='Описание изделия',
        help_text='Напишите об изделии все, что считаете необходимым. Доступны: 1 блок текста; 1 изображение. ',
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('category'),
        FieldPanel('fullname'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

