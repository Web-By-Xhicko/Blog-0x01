from django.db import models
from django.contrib.auth.models import User
from PIL import Image  
from PIL.Image import open

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='Profile.png', upload_to='User_Profile_Picture')
    file_name = models.CharField(max_length=50, blank=True)
    age = models.CharField(max_length=3, default=18)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        self.file_name = self.image.name # Stores the file name
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 350 or img.width > 350:
            resize = (350, 350)
            img.thumbnail(resize)
            img.save(self.image.path)