from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=False)
@stringfilter
def endswith(value: str, suffix):
    return value.endswith(suffix)


@register.filter(is_safe=False)
@stringfilter
def startswith(value: str, suffix):
    return value.startswith(suffix)
