# Aldryn Common

![build status](https://img.shields.io/travis/aldryn/aldryn-common.svg) ![coverage](https://img.shields.io/coveralls/aldryn/aldryn-common.svg) ![PyPI version](https://img.shields.io/pypi/v/aldryn-common.svg)

Aldryn Common is a library of helpful utilities for packages in the [Aldryn](http://aldryn.com) ecosystem, and is
also aimed at developers of [django CMS](http://django-cms.org) projects.

It's installed by default in your Aldryn project - you don't need to do anything to install it - and numerous other
Addons will make use of the tools it provides. Feel free to make use of them in your own projects.

They include tools for:

* pagination
* handling slugs (cleaning, ensuring uniqueness)
* managing times and dates

as well as a variety of helpful templatetags and more.

## Settings:
* ``ALDRYN_COMMON_PAGINATION_SOFTLIMIT``: Soft-limiting search results. If True, querying a page number larger than max.
 will not fail, but instead return the last available page. Default is True.

Requires [Aldryn Boilerplates](https://github.com/aldryn/aldryn-boilerplates)
