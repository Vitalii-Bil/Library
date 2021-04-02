from django.apps import AppConfig


class WharehouseConfig(AppConfig):
    name = 'wharehouse'

    def ready(self):
        import wharehouse.signals  # noqa
