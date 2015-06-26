# Aldryn Common

Aldryn Common is a library of helpful utilities for packages in the [Aldryn](http://aldryn.com) ecosystem.

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
