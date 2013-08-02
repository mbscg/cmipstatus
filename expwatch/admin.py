from django.contrib import admin
from expwatch.models import Exp, ExpMember, Alert

admin.site.register(Exp)
admin.site.register(ExpMember)
admin.site.register(Alert)
