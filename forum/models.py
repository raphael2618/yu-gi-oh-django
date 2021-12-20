import time
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Forum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title) if i want to add time after the slug
        self.slug = slugify(self.title) + '-' + time.strftime("%Y%m%d%H%M%S")
        super(Forum, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
