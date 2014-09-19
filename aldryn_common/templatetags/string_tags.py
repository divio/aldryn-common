# -*- coding: utf-8 -*-
from django import template


register = template.Library()


@register.filter()
def split(value, arg=' '):
    return value.split(arg)
