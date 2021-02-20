from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'app.api.authentication'
    label = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import app.api.authentication.signals
