from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=255)
    expire = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))
    utpdate = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() > self.expire

    def save(self, *args, **kwargs):
        if hasattr(settings, 'TOKEN_EXPIRE'):
            self.expire = timezone.now() + settings.TOKEN_EXPIRE

        super().save(*args, **kwargs)

    def __str__(self):
        return self.token
