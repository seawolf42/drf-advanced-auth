from django.conf import settings


_SETTINGS = getattr(settings, 'DRF_ADVANCED_AUTH', {})


def _get_setting(name, default=None, is_classpath=False):
    value = _SETTINGS.get(name, default)
    return value


AUTH_TOKEN_LIFETIME_MINUTES = _get_setting('AUTH_TOKEN_LIFETIME_MINUTES', default=60 * 24)
