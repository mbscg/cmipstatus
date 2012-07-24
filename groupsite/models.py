from django.db import models
from cmipstatus.models import People

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=4096)
    when = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(People)

    def __unicode__(self):
        return self.title


class NewsImg(models.Model):
    news = models.ForeignKey('News')
    img = models.ImageField(max_length=1024, upload_to='media')


class ScienceThing(models.Model):
    short = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)


class YoutubeVideo(models.Model):
    science_thing = models.ForeignKey('ScienceThing')
    video_link = models.CharField(max_length=1024)
