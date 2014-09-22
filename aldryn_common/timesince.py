import datetime

from django.utils.timezone import is_aware, utc
from django.utils.translation import ungettext, ugettext


def timesince_data(d, now=None, reverse=False):
    """
    Takes two datetime objects and returns the time between d and now
    as a list of components, ordered by size.
    e.g. [{'number': 2, 'type': "hours"}, {'number': 10, 'type': "minutes"}] or
    [
        {'number': 1, 'type': "year"},
        {'number': 8, 'type': "months"},
        {'number': 1, 'type': "week"},
        {'number': 2, 'type': "days"},
        {'number': 9, 'type': "hours"},
        {'number': 42, 'type': "minutes"},
    ].
    If d occurs after now, then [{'number': 0, 'type': "minutes"}] is returned.

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored. Unlike django.utils.timesince,
    all the components are returned as a list of dictionaries.
    """
    chunks = (
        (60 * 60 * 24 * 365, lambda n: ungettext('year', 'years', n)),
        (60 * 60 * 24 * 30, lambda n: ungettext('month', 'months', n)),
        (60 * 60 * 24 * 7, lambda n : ungettext('week', 'weeks', n)),
        (60 * 60 * 24, lambda n : ungettext('day', 'days', n)),
        (60 * 60, lambda n: ungettext('hour', 'hours', n)),
        (60, lambda n: ungettext('minute', 'minutes', n))
    )
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        now = datetime.datetime.now(utc if is_aware(d) else None)

    delta = (d - now) if reverse else (now - d)
    # ignore microseconds
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return []
    r = []
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        r.append({'number': count, 'type': name(count)})
    return r


def timesince_data_nonzero(d, now=None, reverse=False):
    return [item for item in timesince_data(d, now, reverse) if item['number'] > 0]


def timesince_data_single(d, now=None, reverse=False):
    r = timesince_data_nonzero(d, now, reverse)
    if r:
        return r[0]
    else:
        return {'number': 0, 'type': ugettext('minutes')}


def timesince_text(d, now=None):
    return ugettext('%(number)d %(type)s') % timesince_data_single(d, now)[0]


def timeuntil_data(d, now=None):
    return timesince_data(d, now, reverse=True)


def timeuntil_data_nonzero(d, now=None):
    return timesince_data_nonzero(d, now, reverse=True)


def timeuntil_data_single(d, now=None):
    return timesince_data_nonzero(d, now, reverse=True)


def timeuntil_text(d, now=None):
    return ugettext('%(number)d %(type)s') % timeuntil_data_nonzero(d, now)[0]
