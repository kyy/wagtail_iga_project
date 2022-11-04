from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.models import Page


class HomePage(Page):
    # subpage_types = []
    parent_page_types = []
    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Подзаголовок'
    )

    body = StreamField([
        ('txt_block', RichTextBlock()),
    ], use_json_field=True)

    # редактор текста
    txt_edit = RichTextField(
        blank=True,
        null=True,
        verbose_name='Описание сайта',
    )

    # поле ввода в админке
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('txt_edit'),
        FieldPanel('body')
    ]