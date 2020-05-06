from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter
@stringfilter
def formatlines(value):
    stringValue = value
    # Convert every line into a list item
    stringValue = re.sub(r"(^.*)", r"<li>\1</li>", stringValue, 0, re.MULTILINE)
    return stringValue

