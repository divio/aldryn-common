# -*- coding: utf-8 -*-
from django import template
from django.utils.dateformat import format

register = template.Library()


class DateRangeNode(template.Node):
    YEAR_FORMATS = ['y', 'Y']
    MONTH_FORMATS = ['b', 'F', 'M', 'n']
    DAY_FORMATS = ['d', 'j']

    def __init__(self, start_date, end_date, always_show_year=False):
        self.start_date = template.Variable(start_date)
        self.end_date = template.Variable(end_date)
        self.show_year = template.Variable(always_show_year)

    def render(self, context):
        try:
            start_date = self.start_date.resolve(context)
            end_date = self.end_date.resolve(context)
            if self.show_year:
                show_year = self.show_year.resolve(context)
            else:
                show_year = False
        except template.VariableDoesNotExist:
            return ''

        if start_date.year != end_date.year:
            result = u"%s – %s" % (
                format(start_date, 'd.m.Y'), format(end_date, 'd.m.Y'))
            show_year = False
        elif start_date.month != end_date.month:
            result = u"%s – %s" % (
                format(start_date, 'd.m.'), format(end_date, 'd.m.'))
        elif start_date.day != end_date.day:
            result = u"%s.–%s.%s." % (
                format(start_date, 'd'),
                format(end_date, 'd'),
                format(end_date, 'm'),
                )
        else:
            result = format(start_date, 'd.m.')
        if show_year:
            result += format(end_date, 'Y')
        return result


def do_date_range(parser, token):
    chunks = token.split_contents()
    if len(chunks) not in (2, 3, 4):
        raise template.TemplateSyntaxError(
            "%r tag requires one or two arguments" % token.contents.split()[0])
    return DateRangeNode(
        chunks[1],
        chunks[2] if len(chunks) > 2 else chunks[1],
        chunks[3] if len(chunks) == 4 else False
    )

register.tag('date_range', do_date_range)
