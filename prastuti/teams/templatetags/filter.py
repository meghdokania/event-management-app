from django import template

register = template.Library()


@register.filter(name='get_key')
def get_key(dict, key):
    return dict.get(key)