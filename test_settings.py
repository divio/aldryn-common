#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def noop_gettext(s):
    return s


gettext = noop_gettext


HELPER_SETTINGS = {
    'TIME_ZONE': 'UTC',
    'INSTALLED_APPS': [
        'aldryn_boilerplates',
        'sortedm2m',
    ],
    'CMS_PERMISSION': True,
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
    ),
    'CMS_LANGUAGES': {
        'default': {
            'public': True,
            'hide_untranslated': False,
            'fallbacks': ['en']

        },
        1: [
            {
                'public': True,
                'code': 'en',
                'fallbacks': [u'de'],
                'hide_untranslated': False,
                'name': gettext('en'),
                'redirect_on_fallback': True,
            },
            {
                'public': True,
                'code': 'de',
                'fallbacks': [u'en'],
                'hide_untranslated': False,
                'name': gettext('de'),
                'redirect_on_fallback': True,
            },
        ],
    },
    'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
    'DEBUG': True,
    'TEMPLATE_DEBUG': True,
    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    },
    'MIDDLEWARE': [
        'django.middleware.http.ConditionalGetMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
}


def run():
    from djangocms_helper import runner
    runner.run('aldryn_common', extra_args=[])


if __name__ == "__main__":
    run()
