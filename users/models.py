from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    city = models.CharField(
        _("City"), blank=True, max_length=255
    )
    biography = models.TextField(_("Biography"), blank=True)

    def __str__(self):
        return self.username
