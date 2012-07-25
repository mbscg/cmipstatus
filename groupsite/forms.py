from django import forms
from models import News, Post, ScienceThing, YoutubeVideo, NewsImg

class FormNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content', 'long_content')


class FormPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'content')


class FormVideo(forms.Form):
    youtube_link = forms.CharField(max_length=1024)
    short = forms.CharField(max_length=256)
    description = forms.CharField(max_length=2048)


class FormImage(forms.ModelForm):
    class Meta:
        model = NewsImg
        
