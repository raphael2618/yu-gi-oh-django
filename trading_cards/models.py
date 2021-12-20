import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Profile, ProfileType


class Card(models.Model):
    yugioh_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    img = models.URLField()
    img_small = models.URLField()
    desc = models.CharField(max_length=100)
    profiles = models.ManyToManyField(Profile, related_name='deck')

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        origin = random.choice(ProfileType.objects.all())  # remember that ProfileType is empty...
        profile = Profile.objects.create(user=instance, origin=origin)
        profile.deck.add(*random.sample(list(Card.objects.all()), k=26))


class Trade(models.Model):
    STATUS_CHOICES = [('F', 'Finalized'), ('P', 'Pending')]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return self.card.name


class Offer(models.Model):
    STATUS_CHOICES = [("A", "Accepted"), ("D", "Declined"), ("W", "Waiting review")]
    profile = models.ForeignKey(Profile, models.CASCADE)  # because 2nd argument on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, models.CASCADE, related_name='offers')
    card = models.ForeignKey(Card, models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="W")

    def __str__(self):
        return self.card.name
