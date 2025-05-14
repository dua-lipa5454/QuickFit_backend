from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    clothing_image = models.ImageField(upload_to='clothing_images/', blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'phone_number'] 

    def __str__(self):
        return self.username
    
def avatar_file_path(instance, filename):
    return f'avatars/{filename}'  # Ensures unique storage in 'media/avatars/'

class Avatar(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=avatar_file_path)  # Stores files in 'media/avatars/'
    created_at = models.DateTimeField(auto_now_add=True)  # Auto adds timestamp

    def __str__(self):
        return self.name

    @property
    def file_url(self):
        if self.file:
            return self.file.url  # Returns the absolute URL of the file
        return None