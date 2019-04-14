from django import forms
from django.forms import ModelForm
from .models import NewsUsers

 #creating model forms   
class NewsUserForm(forms.ModelForm):
	class Meta:
		model = NewsUsers
		fields = ['name','email']
