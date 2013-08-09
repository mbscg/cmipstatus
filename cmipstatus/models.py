from django.db import models
from django.contrib.auth.models import User


class People(User):
    name = models.CharField(max_length=100, verbose_name="Nome")
    about = models.TextField(default='INPE GMAO Researcher', verbose_name="Sobre")
    photo = models.ImageField(max_length=1048, upload_to='media', 
        default='profile_default.png', verbose_name="Foto")

    def __unicode__(self):
        return self.name
