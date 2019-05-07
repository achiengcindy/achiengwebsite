from django import forms
from .models import Post, Comment
from tinymce.widgets import TinyMCE

class EmailPostForm(forms.Form):
    name=forms.CharField(required=False, max_length=100)
    email=forms.EmailField(required=True)
    to = forms.EmailField()
    comments = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))	

class SearchForm(forms.Form):
	query = forms.CharField() 

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'image', 'body',)


        # widget = {'body': forms.CharField(widget=TinyMCE(attrs={'cols': 80,'rows': 30}))}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('website','body',)
        labels = {'body': ''}
        widgets = {'body': forms.Textarea(attrs={'cols': 80})}


