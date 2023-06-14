from django.apps import AppConfig


class DjlakangConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djbackoffice'

    def ready(self):
        super().ready()
        self.module.autodiscover()
