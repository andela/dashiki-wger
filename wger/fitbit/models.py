from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


@python_2_unicode_compatible
class TokenManager(models.Model):
    """
    Model for fitbit tokens
    """

    access_token = models.CharField(max_length=300)
    refresh_token = models.CharField(max_length=300)
    has_fitbit_integration = models.BooleanField(default=False)
    user = models.OneToOneField(User)

    def __str__(self):
        """
        Return a more human-readable representation
        """
        return "Access token: " + str(self.access_token) +\
               " Refresh token: " + str(self.refresh_token)
