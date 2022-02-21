from django import template
register = template.Library()

@register.filter(name='split')
def split(value, key):
    if value != '':
        a_list = value.split(key)
        map_object = map(int, a_list)
        list_of_integers = list(map_object)
        return list_of_integers
