from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class TrafficUser(models.Model):
	user 		= models.OneToOneField(User)
	birthday	= models.DateField()
	name		= models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

# def create_traffic_user_callback(sender, instance, **kwargs):
# 	user, new 	= TrafficUser.objects.get_or_create(user=instance)

# post_save.connect(create_traffic_user_callback, User)