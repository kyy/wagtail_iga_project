from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.models import Page


class HomePage(Page):
    subpage_types = ['products.ProductIndexPage',
                     'products.ProductTagIndexPage',
                     ]
    # parent_page_types = []

    # редактор текста
    txt_edit = RichTextField(
        blank=True,
        null=True,
        verbose_name='Описание сайта',
    )

    # поле ввода в админке
    content_panels = Page.content_panels + [
        FieldPanel('txt_edit'),
    ]