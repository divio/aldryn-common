# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
import django.db.models
import django.forms


# class ForeignKeyWidget(RelatedFieldWidgetWrapper):
class ForeignKeyWidget(django.forms.fields.Select):
    def render(self, name, value, *args, **kwargs):
        output = super(ForeignKeyWidget, self).render(name, value, *args, **kwargs)
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        if not value:
            return output
        try:
            url = reverse('admin:%s_%s_change' % info, current_app=self.admin_site.name, args=(value,))
        except NoReverseMatch:
            info = (self.admin_site.root_path, rel_to._meta.app_label, rel_to._meta.object_name.lower(), value)
            url = '%s%s/%s/change/%s' % info
        viewlink = '<a href="{}">details</a>'.format(url)
        return mark_safe('%s%s' % (output, viewlink))


class ForeignKeyFormField(django.forms.ModelChoiceField):
    widget = ForeignKeyWidget

    def __init__(self, rel, queryset, *args, **kwargs):
        from django.contrib.admin import site
        kwargs['widget'] = self.widget(rel, site)
        super(ForeignKeyFormField, self).__init__(queryset, *args, **kwargs)


class ForeignKeyModelField(django.db.models.ForeignKey):
    default_field_class = ForeignKeyFormField

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(ForeignKeyModelField, self).formfield(**defaults)
