from django import forms
from models import News, Post

class FormNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content', 'long_content')


class FormPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'content')
