from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'
    verbose_name = 'Planificateur de Rapports'

    def ready(self):
        """Démarre le scheduler au démarrage de l'application."""
        from .scheduler import start_scheduler
        start_scheduler()
