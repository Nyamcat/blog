from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribe = models.BooleanField(default=True)
    alert = models.BooleanField(default=False)
    alert_msg = models.CharField(max_length=300, default=True, null=True, blank=True)

    class Meta:
        db_table = 'auth_user_profile'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class SubscribeTotal(models.Model):
    cnt = models.IntegerField(default=0, null=True, blank=True)
