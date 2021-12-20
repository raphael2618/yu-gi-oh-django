from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    origin = models.ForeignKey('ProfileType', on_delete=models.CASCADE)

    # deck = models.ManyToManyField(Card, related_name='profiles')
    # is_yugi = models.BooleanField()
    # origin = models.CharField(choices=PROFILE_CHOICES, on_delete=models.CASCADE)
    # PROFILE_CHOICES = [
    #     ('Y', 'Yugi'), ('...')
    # ]

    def __str__(self):
        return f"{self.user}"


class ProfileType(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"
