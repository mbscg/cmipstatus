from django.db import models
from cmipstatus.models import People

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=4096)
    long_content = models.TextField(default=" ")
    when = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(People)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class NewsImg(models.Model):
    news = models.ForeignKey('News')
    img = models.ImageField(max_length=1024, upload_to='media')

    def __unicode__(self):
        return self.news.title


class ScienceThing(models.Model):
    short = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.short


class YoutubeVideo(models.Model):
    science_thing = models.ForeignKey('ScienceThing')
    video_link = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.science_thing.short


class Post(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField(default=" ")
    content = models.TextField(default=" ")
    when = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(People)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Publication(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(default="")
    when = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    author = models.ForeignKey(People)
    pdf = models.FileField(max_length=1024, upload_to='publications')

    def __unicode__(self):
        return ', '.join([self.title, self.author.name])



class NetworkInfo(models.Model):
    TWITTER_ICON = '/media/twitter-bird-white-on-blue.png'
    LINKEDIN_ICON = '/media/LinkedIn_IN_Icon_25px.png'
    GOOGLE_PLUS_ICON = '/media/googleplus-logo.png'
    FACEBOOK_ICON = '/media/f_logo.png'
    WEBSITE_ICON = '/media/Web-Site-icon.png'
    LATTES_ICON = '/media/icon_lattes.png'
    GITHUB_ICON = '/media/github-icon.png'
    BITBUCKET_ICON = '/media/Bitbucket.png'

    people = models.ForeignKey(People)
    lattes = models.CharField(max_length=256, blank=True)
    twitter = models.CharField(max_length=256, blank=True)
    linkedin = models.CharField(max_length=256, blank=True)
    google_plus = models.CharField(max_length=256, blank=True)
    github = models.CharField(max_length=256, blank=True)
    bitbucket = models.CharField(max_length=256, blank=True)
    facebook = models.CharField(max_length=256, blank=True)
    site = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return self.people.name


    def social_icons(self):
        social = []
        if self.lattes:
            social.append({'link':self.lattes, 'icon':self.LATTES_ICON})
        if self.linkedin:
            social.append({'link':self.linkedin, 'icon':self.LINKEDIN_ICON})
        if self.bitbucket:
            social.append({'link':self.bitbucket, 'icon':self.BITBUCKET_ICON})
        if self.github:
            social.append({'link':self.github, 'icon':self.GITHUB_ICON})
        if self.twitter:
            social.append({'link':self.twitter, 'icon':self.TWITTER_ICON})
        if self.google_plus:
            social.append({'link':self.google_plus, 'icon':self.GOOGLE_PLUS_ICON})
        if self.facebook:
            social.append({'link':self.facebook, 'icon':self.FACEBOOK_ICON})
        if self.site:
            social.append({'link':self.site, 'icon':self.WEBSITE_ICON})
        return social


class LattesCache(models.Model):
    text = models.TextField(default='')
    people = models.ForeignKey(People)
    last_update = models.DateField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return "cache " + self.people.name


class Editor(models.Model):
    people = models.ForeignKey(People)

    def __unicode__(self):
        return "Editor " + self.people.name
