from django import template

register = template.Library()

@register.filter
def human_file_size(value):
    for x in ['bytes','KiB','MiB','GiB']:
        if value < 1024.0:
            return "%3.2f %s" % (value, x)
        value /= 1024.0
    return "%3.2f %s" % (value, 'TiB')