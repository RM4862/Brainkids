from django.apps import AppConfig


class JuegoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'juego'
    def ready(self):
        import juego.signals
