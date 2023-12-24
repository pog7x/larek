from django import template
from django.template.defaultfilters import stringfilter, floatformat
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(is_safe=False)
@stringfilter
def endswith(value: str, suffix):
    return value.endswith(suffix)


@register.filter(is_safe=False)
@stringfilter
def startswith(value: str, suffix):
    return value.startswith(suffix)


@register.filter(is_safe=True)
def commaprice(value: int):
    return intcomma(floatformat(value, -1))
