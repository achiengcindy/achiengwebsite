from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=25)
    subject = forms.CharField(max_length=30)
    email = forms.EmailField()
    message = forms.CharField(required=False,widget=forms.Textarea)