from django.apps import AppConfig


class AuthTokenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authtoken'

    def ready(self):
        pass
