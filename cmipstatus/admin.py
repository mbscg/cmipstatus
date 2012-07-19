from django.contrib import admin
from cmipstatus.models import Experiment,  Member, People, Comment, ExpReport, MemberReport, ConvReport

admin.site.register(Experiment)
admin.site.register(Member)
admin.site.register(People)
admin.site.register(Comment)
admin.site.register(ExpReport)
admin.site.register(MemberReport)
admin.site.register(ConvReport)
