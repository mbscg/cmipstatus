import cronjobs
from cmipstatus.views import forcefeed

@cronjobs.register
def force_feed():
    forcefeed()
