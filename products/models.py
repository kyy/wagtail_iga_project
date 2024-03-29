import wagtail.models
from django import forms
from django.core.paginator import Paginator
from django.db import models
from django.utils.safestring import mark_safe
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.panels import InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, route
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from taggit.models import Tag
from wagtail.search.models import Query


#constants
max_product_image_numbers = 5
min_product_image_numbers = 1
pagination_number = 6

links = {'new_product_category':
             '<a target="_blank" href="/admin/products/productcategory/create/"> создать категорию.</a>',
}
                        # get all categories with live products:
def live_categories():
    all_products_live_id = ProductPage.objects.live().values_list('categories_id', flat=True)
    list_live_id_uniqe = list(set(all_products_live_id))
    return ProductCategory.objects.filter(id__in=list_live_id_uniqe).order_by('-id')

                        # pagination:
def pagination(request, number_of_pages, model):
    paginator = Paginator(model, number_of_pages)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


class ProductIndexPage(RoutablePageMixin, Page):
    subpage_types = ['ProductPage']
    parent_page_types = ['home.HomePage']
    page_description = "корневая страница для каталога продукции, также откроется по запросу all-categories/"

    def get_context(self, request, *args, **kwargs):
        context = super(ProductIndexPage, self).get_context(request, *args, **kwargs)
        tags_all = Tag.objects.exclude(products_productpagetag_items__content_object__isnull=True)
        context['product_page'] = self
        context['live_categories'] = live_categories
        context['tags_all'] = tags_all
        return context

    def get_tag(self, request):
        tag = request.GET.getlist('tag')
        if tag:
            productpages = ProductPage.objects.filter(tags__slug__in=tag)
        else:
            productpages = self.get_children().live().order_by('-first_published_at')
        return productpages

    @path('')
    def all_category_page(self, request):
        products_page = Page.objects.get(id=ProductIndexPage.objects.first().id)
        return self.render(request, context_overrides={
            'title': products_page.title,
            'productpages': pagination(request, pagination_number, self.get_tag(request)),
        })

    @path('categories/<str:cat_name>/')
    def current_category_page(self, request, cat_name=None):
        tag = request.GET.getlist('tag')
        productpages_cat = ProductPage.objects.live().filter(categories__slug__iexact=cat_name).order_by('-first_published_at')
        if tag:
            productpages = ProductPage.objects.filter(tags__slug__in=tag).filter(categories__slug__iexact=cat_name).order_by('categories__name')
        else:
            productpages = productpages_cat
        current_cat = live_categories().get(slug=cat_name).name
        tag_cat_id = list(set(productpages_cat.values_list('tags', flat=True)))
        tags_all = Tag.objects.exclude(products_productpagetag_items__content_object__isnull=True).filter(id__in=tag_cat_id)
        return self.render(request, context_overrides={
            'title': "%s" % current_cat,
            'tags_all': tags_all,
            'productpages': pagination(request, pagination_number, productpages),
            })

    @route(r"^search/$")
    def post_search(self, request):
        search_query = request.GET.get("q", None)
        if search_query:
            Query.get(search_query).add_hit()
            productpages = ProductPage.objects.live().search(search_query, operator="or")
            title = 'Поиск'
        else:
            productpages = self.get_tag(request)
            title = 'Вся продукция'
        return self.render(request, context_overrides={
            'title': title,
            'query':  search_query,
            'productpages': pagination(request, pagination_number, productpages),
        })

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
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class ProductPage(Page):
    subpage_types = []
    parent_page_types = ['ProductIndexPage']
    page_description = "Пополняйте каталог тут или в разделе - Продукция/Продукция"
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
                                   related_name='name_category',
                                   verbose_name='Категория'
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
                   widget=forms.Select,
                   heading='Категория',
                   help_text=mark_safe('Выберите категорию изделия. Если отсутствует подходящая, вы '
                                        'можете оставить поле пустым или'+links['new_product_category']+
                                        '<br>Расположение категорий: Продукция/Категории продукции/...')
                   ),
        FieldPanel('intro',
                   heading='Полное наименование изделия'
                   ),
        FieldPanel('body',
                   heading='Полное описание',
                   help_text='Описание отображается только на индивидуальной странице.',
                   ),
        InlinePanel('gallery_images',
                    heading='Галерея',
                    label="Изображение",
                    help_text='Первое изображение также будет отображаться в каталоге как превью продукта.'
                              f' Максимальное количество изображений - {max_product_image_numbers}.',
                    max_num=max_product_image_numbers,
                    min_num=min_product_image_numbers,
                    ),
    ]

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукция'


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
    page_description = "Корневая страница ведущая к запросу фильтр-тег"
    max_count = 1

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_context(self, request):
        # Фильтр по тегам
        tag = request.GET.get('tag')
        productpages = ProductPage.objects.filter(tags__slug=tag).order_by('categories__name')
        tags_all =  Tag.objects.exclude(products_productpagetag_items__content_object__isnull=True)

        # Обновление контекста шаблона
        context = super().get_context(request)
        context['productpages'] = productpages
        context['tags_all'] = tags_all
        return context


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    prepopulated_fields = {"slug": ("name",)}
    panels = [
        FieldPanel('name',
                   help_text='Данная категория будет доступна при пополнении каталога продукции',
                   heading='Имя категории'
                   ),
        FieldPanel('icon',
                   help_text='Выберите визуальный образ характеризующий категорию',
                   heading='Иконка категории'
                   ),
        FieldPanel('slug',
                   help_text='Cсылка категории',
                   heading='Слаг'
                   ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории каталога продукции'

