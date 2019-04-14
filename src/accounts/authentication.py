from django.contrib.auth.models import User


# see https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username

class EmailAuthBackend:
	def authenticate(self, request,username=None, password=None):
		try:
			user = User.objects.get(email=username)
			if user.check_password(password):
				return user
			return None
		except User.DoesNotExist:
			return None
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
