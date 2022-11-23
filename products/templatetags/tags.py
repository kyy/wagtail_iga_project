from django import template
from products.models import live_categories

register = template.Library()


@register.inclusion_tag('products/tags/live_categories.html', takes_context=True)
def live_categories_menu(context):
    return {
        'live_categories': live_categories,
        'request': context['request'],
    }

@register.inclusion_tag('products/tags/live_categories_burger_menu.html', takes_context=True)
def live_categories_burger_menu(context):
    return {
        'live_categories': live_categories,
        'request': context['request'],
    }