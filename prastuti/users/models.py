from django.db import models
from django.contrib.auth.models import User


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
