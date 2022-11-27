import requests
from django.core.exceptions import ValidationError
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock
from wagtail.models import Page
from django.contrib import messages



class HomePage(Page):
    subpage_types = ['products.ProductIndexPage',
                     'products.ProductTagIndexPage',
                     'Settings',
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


url = 'https://jenil.github.io/bulmaswatch/api/themes.json'
bulma = requests.get(url).json()
name = []
css = []
for i in range(len(bulma['themes'])):
    css.append(bulma['themes'][i]['css'])
    name.append(bulma['themes'][i]['name'])
CSS_NAMES = tuple(zip(css, name))


class Settings(Page):
    parent_page_types = ['HomePage']
    subpage_types = []
    page_description = "Настройки сайта"
    max_count = 1

    url_bulma_css = models.URLField(max_length=255, unique=True, choices=CSS_NAMES, default=CSS_NAMES[4])
    content_panels = Page.content_panels + [
        FieldPanel('url_bulma_css',
                   help_text='BULMA CSS стили',
                   ),
    ]
    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'








