from django.db import models

RESTART_LIST_DEFAULT = ' '

class Exp(models.Model):
    name = models.CharField(max_length=15)
    members = models.IntegerField(default=1)

    def __unicode__(self):
        return ', '.join([self.name, str(self.members)])


class ExpMember(models.Model):
    exp = models.ForeignKey('Exp')
    member = models.IntegerField(default=0)
    restart_list = models.CharField(max_length=1024, default=RESTART_LIST_DEFAULT)
    description = models.TextField(max_length=1024, default=' ')
