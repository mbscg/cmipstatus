from django.contrib import admin
from inpe.cmipstatus.models import Experiment, TupaQuery, Member

admin.site.register(Experiment)
admin.site.register(Member)
admin.site.register(TupaQuery)
