from django.apps import AppConfig


class Config(AppConfig):

    name = 'drf_advanced_auth'
    verbose_name = 'DRF Advanced Auth'

    def ready(self):
        pass
