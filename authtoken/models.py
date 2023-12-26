from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token
