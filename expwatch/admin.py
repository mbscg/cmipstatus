from django.contrib import admin
from expwatch.models import Exp, ExpMember, Alert, MemberConfig

admin.site.register(Exp)
admin.site.register(ExpMember)
admin.site.register(MemberConfig)
admin.site.register(Alert)
