from django import template

register = template.Library()

@register.filter
def multiply(val, arg):
    try:
        return float(val) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def float_add(val, arg):
    try:
        return float(val) + float(arg)
    except (ValueError, TypeError):
        return ''
