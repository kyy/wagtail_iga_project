import os
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from products.models import ProductCategory, ProductPage
from django.db.models.signals import  post_save
from django.dispatch import receiver
from wagtail.images import get_image_model

#constant
IMAGE_MODEL= get_image_model()

@receiver(post_save, sender=IMAGE_MODEL)
def optimize_image_storage(sender, instance, created=False, **kwargs):
    if created:
        croped_image = instance.get_rendition('max-2000x2000|jpegquality-80')
        croped_file = croped_image.file.path
        original_file = instance.file.path
        copy_o_f = original_file
        try:
            os.rename(croped_file, original_file)
        except FileExistsError:
            os.remove(original_file)
            os.rename(croped_file, copy_o_f)
        instance.width = croped_image.width
        instance.height = croped_image.height
        instance.file_size = os.path.getsize(original_file)
        instance.save()


class ProductCategoryAdmin(ModelAdmin):
    model = ProductCategory
    menu_icon = 'table'
    menu_label = 'Категории продукции'
    add_to_settings_menu = False
    exclude_from_explorer = False
    search_fields = ('name', 'slug')
    list_display = ('name', 'slug', 'icon')
    inspect_view_enabled = True
    prepopulated_fields = {'slug': ['name']}


class ProductPageAdmin(ModelAdmin):
    model = ProductPage
    menu_icon = 'table'
    menu_label = 'Продукция'
    add_to_settings_menu = False
    exclude_from_explorer = False
    search_fields = ('title',)
    inspect_view_enabled = True
    list_display = ('title', 'slug', 'seo_title', 'categories', 'latest_revision_created_at', 'url_path', 'live')


class ElementAdminGroup(ModelAdminGroup):
    menu_label = "Элементы сайта"
    items = (ProductCategoryAdmin, ProductPageAdmin)
    menu_order = 200


modeladmin_register(ElementAdminGroup)