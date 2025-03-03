from django import template

register = template.Library()

@register.inclusion_tag('judul_template.html')
def add_judul(takes_context = True):
    return {'name': 'Rachmat Gunawan'}