from django import template

register = template.Library()

@register.filter
def cortar_texto(texto, limite):
    if not texto:  # Verifica se o texto é None ou vazio
        return ''
    if len(texto) <= limite:
        return texto
    corte = texto.rfind(' ', 0, limite)
    if corte == -1:
        return texto[:limite] + ' ...'
    return texto[:corte] + ' ...'


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
