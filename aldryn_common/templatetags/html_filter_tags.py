# -*- coding: utf-8 -*-
from django import template
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


@register.filter()
def html_strong(value, safe=False):
    if not safe:
        value = escape(value)
    return mark_safe(u"<strong>%s</strong>" % value)


@register.filter()
def safe_html_strong(value):
    # same as html_strong, but treat value as safe
    return html_strong(value, safe=True)


@register.filter()
def html_make_anchortag(value, arg=None, safe=False):
    # TODO: for some weird reason "&" in href in the template even for valid
    #       urls and with the mark_safe. The resulting string of this
    #       filter looks correct... but...??!?
    href = value
    try:
        # this must always be a valid url. otherwise it might be used for XSS
        # but we cant blindly escape it, because it may contain "&" which is ok.
        URLValidator(href)
    except ValidationError:
        href = escape(href)
    label = arg or href
    if not safe:
        label = escape(label)
    return mark_safe(u'''<a href="%s">%s</a>''' % (href, label))


@register.filter()
def safe_html_make_anchortag(value, arg=None):
    return html_make_anchortag(value, arg=arg, safe=True)


@register.filter()
def html_make_mail_anchortag(value, arg=None):
    email = value
    label = arg or email
    return mark_safe(u'''<a href="mailto:%s">%s</a>''' % (email, label))
