from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    RACE_TYPES = (
        ('FM', 'full marathon'),
        ('HM', 'half marathon'),
        ('FK', '5k')
    )

    user = models.OneToOneField(User)
    race_type = models.CharField(max_length=2,choices=RACE_TYPES)

    def __unicode__(self):
        return self.user.username
