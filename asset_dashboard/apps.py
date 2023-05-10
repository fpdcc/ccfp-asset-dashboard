from django.apps import AppConfig


class DjangoAppConfig(AppConfig):
    name = 'asset_dashboard'

    def ready(self):
        import asset_dashboard.signals  # noqa
