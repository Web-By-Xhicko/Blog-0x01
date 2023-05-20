from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='Profile.png', upload_to='User_Profile_Picture')
    age = models.CharField(max_length=3, default=18)
    bio = models.TextField(max_length=150, default='My Bio says...')

    def __str__(self):
        return f'{self.user.username} profile'
