from django.db import models


def user_directory_path(instance, filename):
    return 'uploado_photos/{0}/{1}'.format(instance.user.id, filename)
# Create your models here.
class Photo(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth_api.CustomUser', on_delete=models.CASCADE)
    # title = models.CharField(max_length=100)
    # description = models.TextField()
    image = models.ImageField(upload_to=user_directory_path)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
