from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,)
	birth_date = models.DateField(blank=True, null=True, help_text='Please use the following format: YYYY-MM-DD.',)
	photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)
	# contact info
	phone = models.CharField(max_length=20)
	#shipping information
	physical_address =  models.CharField(max_length=250)
	postal_code = models.CharField(max_length=20)
	city = models.CharField(max_length=100)
	Estate = models.CharField(max_length=100)


	def __str__(self):
		return 'Profile of user: {}'.format(self.user.username)

#create a user profile  when user is created
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)
