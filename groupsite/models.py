# -*- encoding: utf-8 -*-

from django.db import models
from cmipstatus.models import People
from django.contrib.syndication.views import Feed


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.CharField(max_length=4096, verbose_name="Descrição")
    long_content = models.TextField(default=" ", verbose_name="Conteúdo")
    when = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(People)
    approved = models.BooleanField(default=False)
    besm = models.BooleanField(default=False)

    def get_absolute_url(self):
        return "http://antares.ccst.inpe.br/gmao/news/{0}".format(self.id)

    def __unicode__(self):
        return self.title


class NewsImg(models.Model):
    news = models.ForeignKey('News', verbose_name="Notícia")
    img = models.ImageField(max_length=1024, upload_to='media', verbose_name="Imagem")
    description = models.TextField(default='')

    def __unicode__(self):
        return self.news.title


class NewsAttachment(models.Model):
    news = models.ForeignKey('News', verbose_name="Notícia")
    attachment = models.FileField(max_length=1024, upload_to='attachments', verbose_name="Arquivo")
    description = models.TextField(default='')

    def __unicode__(self):
        return self.attachment.__unicode__()


class ScienceThing(models.Model):
    short = models.CharField(max_length=256, verbose_name="Título")
    description = models.CharField(max_length=2048, verbose_name="Descrição")
    approved = models.BooleanField(default=False)
    besm = models.BooleanField(default=False)

    def __unicode__(self):
        return self.short


class YoutubeVideo(models.Model):
    science_thing = models.ForeignKey('ScienceThing')
    video_link = models.CharField(max_length=1024, verbose_name="Link do Vídeo (embed)")

    def __unicode__(self):
        return self.science_thing.short


class Post(models.Model):
    title = models.CharField(max_length=512, verbose_name="Título")
    description = models.TextField(default=" ", verbose_name="Descrição")
    content = models.TextField(default=" ", verbose_name="Conteúdo")
    using_markdown = models.BooleanField(default=False, verbose_name="Usando Markdown?")
    when = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(People)
    approved = models.BooleanField(default=False)
    besm = models.BooleanField(default=False)

    def get_absolute_url(self):
        return "http://antares.ccst.inpe.br/gmao/posts/{0}".format(self.id)


    def __unicode__(self):
        return self.title


class PostImg(models.Model):
    post = models.ForeignKey('Post', verbose_name="Post")
    img = models.ImageField(max_length=1024, upload_to='media', verbose_name="Imagem")
    description = models.TextField(default='')

    def __unicode__(self):
        return self.post.title


class PostAttachment(models.Model):
    post = models.ForeignKey('Post', verbose_name="Post")
    attachment = models.FileField(max_length=1024, upload_to='attachments', verbose_name="Arquivo")
    description = models.TextField(default='')

    def __unicode__(self):
        return self.attachment.__unicode__()
    

class Publication(models.Model):
    title = models.CharField(max_length=256, verbose_name="Título")
    description = models.TextField(default="", verbose_name="Descrição")
    when = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField(verbose_name="Data de Publicação")
    author = models.ForeignKey(People)
    pdf = models.FileField(max_length=1024, upload_to='publications', verbose_name="Arquivo")
    besm = models.BooleanField(default=False)

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


class PostsFeed(Feed):
    title = "GMAO Blog Feed"
    link = "http://antares.ccst.inpe.br/gmao/blog/"
    description = "Latest posts from GMAO team"
    description_template = "gmaofeedtemplate.html"

    def items(self):
        return Post.objects.order_by('-when')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content


class NewsFeed(Feed):
    title = "GMAO News Feed"
    link = "http://antares.ccst.inpe.br/gmao/news/"
    description = "Latest news from GMAO"

    def items(self):
        return News.objects.order_by('-when')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.long_content
