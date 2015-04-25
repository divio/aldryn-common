# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from itertools import chain
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
import django.db.models
import django.forms
from django.conf import settings
import sortedm2m.fields
import sortedm2m.forms


class SortedM2MWidget(sortedm2m.forms.SortedCheckboxSelectMultiple):
    template = 'admin/aldryn_common/widgets/sortedm2m_widget.html'

    def render(self, name, value, attrs=None, choices=()):
        # TODO: make a pull request to sortedm2m to make it easy to override the template
        # TODO: make a pull request to sortedm2m to make it easy to add the addtional link to admin (or integrate this whole widget)
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)

        # Normalize to strings
        str_values = [force_text(v) for v in value]

        selected = []
        unselected = []

        # get the admin link
        rel_to = self.choices.queryset.model  # this is hacky
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())

        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = ' for="%s"' % conditional_escape(final_attrs['id'])
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_text(option_label))

            try:
                admin_url = reverse(
                    'admin:%s_%s_change' % info,
                    # current_app=self.admin_site.name,
                    args=(option_value,),
                )
            except NoReverseMatch:
                info = (
                    self.admin_site.root_path,
                    rel_to._meta.app_label,
                    rel_to._meta.object_name.lower(),
                    option_value,
                )
                admin_url = '%s%s/%s/change/%s' % info
            # admin_url = (
            #     u'<a href="%s" style="margin-left:10px;"><img src="%sadmin/img/admin/icon_changelink.gif" '
            #     u'width="10" height="10" alt="View current"/></a>'
            # ) % (url, settings.STATIC_URL)
            item = {
                'label_for': label_for,
                'rendered_cb': rendered_cb,
                'option_label': option_label,
                'option_value': option_value,
                'admin_url': admin_url,
            }

            if option_value in str_values:
                selected.append(item)
            else:
                unselected.append(item)

        # re-order `selected` array according str_values which is a set of `option_value`s in the order they should be shown on screen
        ordered = []
        for value in str_values:
            for select in selected:
                if value == select['option_value']:
                    ordered.append(select)
        selected = ordered

        html = render_to_string(
            self.template,
            {'selected': selected, 'unselected': unselected})
        return mark_safe(html)


class SortedM2MFormField(sortedm2m.fields.SortedMultipleChoiceField):
    widget = SortedM2MWidget

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = self.widget
        super(SortedM2MFormField, self).__init__(*args, **kwargs)


class SortedM2MModelField(sortedm2m.fields.SortedManyToManyField):
    default_field_class = SortedM2MFormField

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(SortedM2MModelField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [
        "^aldryn_common\.admin_fields\.sortedm2m\.SortedM2MModelField"])
except:
    # If South not installed, then we really don't need to have done this.
    pass
