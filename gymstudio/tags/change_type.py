from django import template
register = template.Library()

@register.simple_tag
def change_type(val=''):
    return int(val)