from django.db import models

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

#--Profile with signals that create it on user creation--
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    #picture = models.ImageField(,blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
#--end of profile-- 

class Conversation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', blank=True, null=True)
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=40, default="Conversation")
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message_content = models.TextField(max_length=600)
    sent_date = models.DateTimeField('date sent')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender',blank=True, null=True)

    class Meta:
        ordering = ('-sent_date',)



# Create your models here.
