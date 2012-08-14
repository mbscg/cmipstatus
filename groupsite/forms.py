# -*- encoding: utf-8 -*-

from django import forms
from models import News, Post, ScienceThing, YoutubeVideo, NewsImg
from models import Publication, NetworkInfo, NewsAttachment
from models import PostImg, PostAttachment
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date


class FormNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content', 'long_content', 'besm')


class FormPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'content', 'besm')


class FormVideo(forms.Form):
    youtube_link = forms.CharField(max_length=1024, label="Link Youtube")
    short = forms.CharField(max_length=256, label="Título")
    description = forms.CharField(max_length=2048, label="Descrição")


class FormImage(forms.ModelForm):
    class Meta:
        model = NewsImg


class FormAttachment(forms.ModelForm):
    class Meta:
        model = NewsAttachment


class FormPostImage(forms.ModelForm):
    class Meta:
        model = PostImg


class FormPostAttachment(forms.ModelForm):
    class Meta:
        model = PostAttachment


class FormPublication(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title', 'description', 'publication_date', 'pdf', 'besm')


class FormNetwork(forms.ModelForm):
    class Meta:
        model = NetworkInfo
        exclude = ('people',)
