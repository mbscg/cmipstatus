from django.contrib import admin
from groupsite.models import News, NewsImg, ScienceThing, YoutubeVideo
from groupsite.models import Post, Publication, NetworkInfo, LattesCache
from groupsite.models import Editor, NewsAttachment, PostImg, PostAttachment
from groupsite.models import Graphic, AmbarReport, AmbarPeople

admin.site.register(News)
admin.site.register(NewsImg)
admin.site.register(NewsAttachment)
admin.site.register(ScienceThing)
admin.site.register(YoutubeVideo)
admin.site.register(Graphic)
admin.site.register(Post)
admin.site.register(PostImg)
admin.site.register(PostAttachment)
admin.site.register(Publication)
admin.site.register(NetworkInfo)
admin.site.register(LattesCache)
admin.site.register(Editor)
admin.site.register(AmbarReport)
admin.site.register(AmbarPeople)
