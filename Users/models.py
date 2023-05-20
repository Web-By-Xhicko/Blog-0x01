from django.db import models
from django.contrib.auth.models import User
from PIL import Image  
from PIL.Image import open

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='Profile.png', upload_to='User_Profile_Picture')
    age = models.CharField(max_length=3, default=18)
    bio = models.TextField(max_length=150, default='My Bio says...')

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 350 or img.width > 350:
            resize = (350, 350)
            img.thumbnail(resize)
            img.save(self.image.path)