from __future__ import unicode_literals

from django.template import Context, Template
from django.test import TestCase


class QueryStringTagTest(TestCase):

    TEMPLATE_PREFIX = "{% load query_string_tools %}"

    def tag_template(self, tag_str):
        return Template('{prefix}{tag}'.format(prefix=self.TEMPLATE_PREFIX,
                                               tag=tag_str))

    def test_dictionary_merging(self):
        ctx = {
            'q_str': {'tag': ['a', 'b'], 'year': 2011, 'month': 2},
            'tags': ['c', 'd'],
            'm': 4,
        }
        template = self.tag_template(
            '{% query_string q_str tag+tags month=m %}')
        rendered = template.render(Context(ctx))
        rendered_args = rendered.lstrip('?').split('&')
        expected_args = [
            'year=2011', 'tag=a', 'tag=b', 'tag=c', 'tag=d', 'month=4']
        self.assertEquals(sorted(expected_args), sorted(rendered_args))
