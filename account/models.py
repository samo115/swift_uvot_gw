from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    too_username = models.CharField(max_length=30, blank=True)
    too_secret = models.CharField(max_length=30, blank=True)

#    def __str__(self):
#        return str(self.user)
    # add additional fields in here
    USERNAME_FIELD='user'
    
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()
   
# Create your models here.
