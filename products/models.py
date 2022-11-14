from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.panels import InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet




#constants
max_product_image_numbers = 5
links = {'new_product_category':
             '<a target="_blank" href="/admin/snippets/products/productcategory/add/"> создать категорию.</a>',
}


class ProductIndexPage(Page):
    subpage_types = ['ProductPage']
    parent_page_types = ['home.HomePage']

    # Обновляем контекст для внесения только опубликованных постов в обратном хронологическом порядке
    def get_context(self, request):
        context = super().get_context(request)
        category = request.GET.get('category')

        try:
            # Look for the blog category by its slug.
            cat = ProductPage.objects.get(slug=category)
        except Exception:
            # Blog category doesnt exist (ie /blog/category/missing-category/)
            # Redirect to self.url, return a 404.. that's up to you!
            cat = None

        if cat is None:
            # This is an additional check.
            # If the category is None, do something. Maybe default to a particular category.
            # Or redirect the user to /blog/ ¯\_(ツ)_/¯
            pass

        if category:
            productpages = ProductPage.objects.live().filter(categories__name=category).order_by('-first_published_at')
        else:
            productpages = self.get_children().live().order_by('-first_published_at')
        context['productpages'] = productpages
        return context

    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class ProductPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProductPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ProductPage(Page):
    subpage_types = []
    parent_page_types = ['products.ProductIndexPage']
    page_description = "Пополните каталог используя эту страницу"

    Page._meta.get_field("title").help_text = 'Данное имя может отображаться как заголовок.'

    # даем доступ к изображениям на странице
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ProductPageTag,
                                  blank=True
                                  )
    categories = models.ForeignKey('products.ProductCategory',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   related_name='name_category'
                                   )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('tags',
                   help_text='Краткая характеристика в виде тегов',
                   ),
        FieldPanel('categories',
                   widget=forms.RadioSelect,
                   heading='Категория',
                   help_text= mark_safe('Выберите категорию изделия. Если отсутствует подходящая, вы '
                                        'можете оставить поле пустым или'+links['new_product_category']+
                                        '<br>Располодение категорий: Фрагменты/Категории каталога продукции/...')
                   ),
        FieldPanel('intro',
                   heading = 'Полное наименование изделия'
                   ),
        FieldPanel('body',
                   heading='Полное описание',
                   help_text ='Описание отображается только на индивидуальной странице.',
                   ),
        InlinePanel('gallery_images',
                    heading='Галерея',
                    label="Изображение",
                    help_text='Первое изображение также будет отображаться в каталоге.'
                              f' Максимальное уоличество изображений - {max_product_image_numbers}.',
                    max_num=max_product_image_numbers
                    ),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(ProductPage, on_delete=models.CASCADE,
                       related_name='gallery_images',
                       )
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE,
                              related_name='+',
                              )
    caption = models.CharField(blank=True,
                               max_length=250,
                               )
    panels = [
        FieldPanel('image', heading='Превью'),
        FieldPanel('caption', heading='Подпись'),
    ]


class ProductTagIndexPage(Page):
    subpage_types = []
    parent_page_types = ['home.HomePage']


    def get_context(self, request):
        # Фильтр по тегам
        tag = request.GET.get('tag')
        productpages = ProductPage.objects.filter(tags__name=tag)

        # Обновление контекста шаблона
        context = super().get_context(request)
        context['productpages'] = productpages
        return context


@register_snippet
class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name',
                   help_text='Данная категория будет доступна при пополнении каталога продукции',
                   heading='Имя категории'
                   ),
        FieldPanel('icon',
                   help_text='Выберите визуальный образ характеризующий категорию',
                   heading='Иконка категории'
                   ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории каталога продукции'







