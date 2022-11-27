from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from home.models import Settings


class SettingsAdmin(ModelAdmin):
    model = Settings
    menu_label = "Настройки"
    menu_icon = "tag"
    list_display = ["url_bulma_css",]
    search_fields = ("url_bulma_css",)

    def __str__(self):
        return 'Настройки'



class ElementAdminGroup(ModelAdminGroup):
    menu_label = "Визуал"
    items = (SettingsAdmin,)
    menu_order = 300

modeladmin_register(ElementAdminGroup)