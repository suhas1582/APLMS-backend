from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    roll_no = models.IntegerField(blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    auth_token = models.CharField(max_length=40, default='0')
    dob = models.DateField(blank=True, null=True)
    standard = models.IntegerField(blank=True, null=True)
    section = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self) -> str:
        return self.first_name if self.first_name else 'Anonymous'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

