from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from products.models import ProductCategory, ProductPage


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