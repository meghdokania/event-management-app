from django.db import models
from django.contrib.auth import get_user_model
# from ..events/models import Event

User = get_user_model()

class Team(models.Model):
    members = models.ManyToManyField(User)
    # events = models.ManyToManyField(Event)

    # class Meta:
    #     unique_together = (me)
    def def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('teams:teamdetail', kwargs={'pk': self.pk})
    

