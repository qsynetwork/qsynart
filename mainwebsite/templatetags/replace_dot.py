from django import template

register = template.Library()

@register.filter
def replace_dot(value):
    return value.replace(".","").replace(" ","")