from importlib import import_module

from django.conf import settings


_SETTINGS = getattr(settings, 'DRF_ADVANCED_AUTH', {})


def _load_class(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def _get_setting(name, default=None, is_classpath=False):
    value = _SETTINGS.get(name, default)
    if value and is_classpath:
        value = _load_class(value)
    return value


AUTH_TOKEN_LIFETIME_MINUTES = _get_setting('AUTH_TOKEN_LIFETIME_MINUTES', default=60 * 24)
LOGIN_SUCCESS_RESPONSE_SERIALIZER = _get_setting('LOGIN_SUCCESS_RESPONSE_SERIALIZER', is_classpath=True)
