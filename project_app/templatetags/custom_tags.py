from __future__ import absolute_import
from django import template

register = template.Library()


@register.simple_tag
def object_to_text(text):
    return str(text)
