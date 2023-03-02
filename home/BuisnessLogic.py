import requests


def BULMA_CSS():
    url = 'https://jenil.github.io/bulmaswatch/api/themes.json'
    bulma = requests.get(url).json()
    name = []
    css = []
    for i in range(len(bulma['themes'])):
        css.append(bulma['themes'][i]['css'])
        name.append(bulma['themes'][i]['name'])
    CSS_NAMES = tuple(zip(css, name))
    return CSS_NAMES


