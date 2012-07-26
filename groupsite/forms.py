from django import forms
from models import News, Post, ScienceThing, YoutubeVideo, NewsImg, Publication
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date


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


class FormPublication(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title', 'description', 'publication_date', 'pdf')
        
