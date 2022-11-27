import requests
from django import template
from home.models import Settings

register = template.Library()


@register.inclusion_tag('home/tags/CSS.html', takes_context=True)
def CSS(context):
    url = 'https://jenil.github.io/bulmaswatch/api/themes.json'
    bulma = requests.get(url).json()
    list = []
    for i in range(len(bulma['themes'])):
        list.append(bulma['themes'][i])
    return {
        'bulma': list,
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/CSS_link.html', takes_context=True)
def CSS_link(context):
    try:
        css_link = Settings.objects.live().get().url_bulma_css
    except: css_link = ''
    return {
        'css_link': css_link,
        'request': context['request'],
    }



