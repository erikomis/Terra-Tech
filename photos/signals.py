import os
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from photos.models import Photo

def delete_photo(instance, **kwargs):
    try:
        os.remove(instance.image.path)
    except (FileNotFoundError, ValueError):
        print()
@receiver(pre_delete, sender=Photo)
def delete_file(sender, instance, **kwargs):
    old_instance = sender.objects.get(pk=instance.pk)
    delete_photo(old_instance)
