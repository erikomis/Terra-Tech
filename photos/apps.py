from django.apps import AppConfig


class PhotosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photos'

    def ready(self, *args, **kwargs) -> None:
        import photos.signals
        super_ready = super().ready( *args, **kwargs)
        return super_ready