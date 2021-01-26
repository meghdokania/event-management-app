from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    institute = models.CharField(max_length=250)
    year = models.IntegerField()  # needs validation? ON_HOLD

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('users:{self.user.username}', kwargs={})


# added signals
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
