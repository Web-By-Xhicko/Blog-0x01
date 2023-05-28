from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
       profile = Profile.objects.create(user=instance)
    if  created and not instance.first_name and not instance.last_name:
        instance.first_name = 'First_Name'
        instance.last_name = 'Last_Name'
        instance.save()
            
@receiver(post_save, sender=User)
def save_profile(sender, instance,  **kwargs):
    instance.profile.save()
