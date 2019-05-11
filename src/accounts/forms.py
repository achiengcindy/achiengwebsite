from django import forms
from django.contrib.auth.models import User
from .models import Profile



class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.CharField(label='Password', widget=forms.PasswordInput,  help_text='Password must be six characters long')
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput,  help_text='Password must be six characters long')

    class Meta:
        model = User
        fields = ('username','email','first_name',) 

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email,that is already taken')
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user'),



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'last_name', )


