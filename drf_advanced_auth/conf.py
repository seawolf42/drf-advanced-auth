from django.conf import settings


_SETTINGS = getattr(settings, 'DRF_ADVANCED_AUTH', {})

AUTH_TOKEN_LIFETIME_MINUTES = _SETTINGS.get('AUTH_TOKEN_LIFETIME_MINUTES', 60 * 24)
