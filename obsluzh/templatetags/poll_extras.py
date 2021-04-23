from django import template
from obsluzh.models import *

register = template.Library()


@register.filter(name='to_url')
def to_url(value):
    return value.replace(" ", "_")

