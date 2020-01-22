from django import template
register = template.Library()

@register.filter
def number_format(number):
    return format(number,',')

@register.filter
def get_total(pk):
    pass
