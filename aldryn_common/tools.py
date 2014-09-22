from django.conf import settings


def get_additional_styles(settings_name):
    """
    Get additional styles choices from settings
    """
    choices = []
    raw = getattr(settings, settings_name, False)

    if raw:
        raw_choices = raw.split(',')
        for choice in raw_choices:
            clean = choice.strip()
            choices.append((clean.lower(), clean.title()))
    return choices
