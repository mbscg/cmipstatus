from django.contrib import admin
from groupsite.models import News, NewsImg, ScienceThing, YoutubeVideo
from groupsite.models import Post, Publication, NetworkInfo, LattesCache

admin.site.register(News)
admin.site.register(NewsImg)
admin.site.register(ScienceThing)
admin.site.register(YoutubeVideo)
admin.site.register(Post)
admin.site.register(Publication)
admin.site.register(NetworkInfo)
admin.site.register(LattesCache)
