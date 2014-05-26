import math

from django import template


register = template.Library()


@register.filter
def is_numeric(value):
    try:
        float(value)

        if math.isnan(value):
            return False

        return True
    except ValueError:
        return False
