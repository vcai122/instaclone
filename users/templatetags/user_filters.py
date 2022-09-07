from django import template

register = template.Library()

@register.filter
def get_first_of_dict(value):
    return list(value.values())[0][0]