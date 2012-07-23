from django.db import models
from cmipsite.cmipstatus.models import People

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

