from django.contrib import admin
from inpe.cmipstatus.models import Experiment, TupaQuery

admin.site.register(Experiment)
admin.site.register(TupaQuery)
