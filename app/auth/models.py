from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    from .models import Profile
    if created:
        Profile.objects.create(user=instance)
class Position(models.Model):
    name = models.CharField(max_length=100, blank=True)
    basisentschaedigung = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sitzungsgeld = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    basis_abgabe = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sitzungsabgabe = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name or "Position"
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    geburtsdatum = models.DateField(null=True, blank=True)
    telefonnummer = models.CharField(max_length=20, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name="profiles")

    def __str__(self):
        return self.user.username
