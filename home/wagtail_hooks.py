from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from home.models import HomePage


class SettingsAdmin(ModelAdmin):
    model = HomePage
    inspect_view_enabled = True
    menu_label = "Главная"
    menu_icon = "doc-empty"
    list_display = ["title", "url_bulma_css", 'live',]



    def __str__(self):
        return 'Главная'



class ElementAdminGroup(ModelAdminGroup):
    menu_label = "Визуал"
    items = (SettingsAdmin,)
    menu_order = 200



modeladmin_register(ElementAdminGroup)