from django.db import models
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.panels import TabbedInterface, ObjectList
from wagtail.core.fields import RichTextField
from wagtail.models import Page
from .BuisnessLogic import BULMA_CSS


class HomePage(Page):
    max_count = 1
    subpage_types = ['products.ProductIndexPage',
                     'products.ProductTagIndexPage',
                     ]

    url_bulma_css = models.URLField(max_length=255, unique=True, choices=BULMA_CSS(), default=BULMA_CSS()[4])
    txt_edit = RichTextField(
        blank=True,
        null=True,
        verbose_name='Описание сайта',
    )

    content_panels = Page.content_panels + [
        FieldPanel('txt_edit'),
    ]

    settings_panels = [
        FieldPanel('url_bulma_css',
                   heading='CSS стили @bulmaswatch',
                   help_text=mark_safe('<a target="_blank" href="https://jenil.github.io/bulmaswatch/">Примеры стилей</a>'),
                   ),
    ]

    edit_handler = TabbedInterface([
            ObjectList(Page.content_panels, heading='Содержимое'),
            ObjectList(Page.promote_panels, heading='Продвижение'),
            ObjectList(settings_panels, heading='Настройки' ),
         ]
    )

    class Meta:
        verbose_name = 'Главная страница'

    def __str__(self):
        return HomePage.title



