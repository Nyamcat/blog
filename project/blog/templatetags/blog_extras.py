from django import template

register = template.Library()


@register.filter
def get_full_name(value):
    return value.last_name + value.first_name
