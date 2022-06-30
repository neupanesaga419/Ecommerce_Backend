from django.apps import AppConfig


class NfsdataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NFSDATA'
    
    def ready(self):
        import NFSDATA.signals