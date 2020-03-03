from django import template
register = template.Library()

@register.filter
def number_format(number):
    return format(number,',')

@register.filter
def get_total(pk):
    pass
@register.filter
def get_text(text):
    if len(text) > 74:
        return text[:75]+"..."
    return text    

