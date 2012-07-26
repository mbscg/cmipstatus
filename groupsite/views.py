from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from cmipstatus.models import People
import os
from models import News, NewsImg, ScienceThing, YoutubeVideo, Post, Publication
from cmipstatus.forms import FormEditProfile, FormPassword
from forms import FormNews, FormPost, FormVideo, FormImage, FormPublication


# PUBLIC VIEWS SECTION


def home(request):
    return render_to_response("gmaohome.html", 
        {'imgs':get_imgs_news(), 'news':get_news(latest=True),
         'sciences':get_sciences(latest=True), 'posts':get_posts(latest=True),
         'user':request.user}
        )

def news(request):
    return render_to_response("gmaonews.html",
        {'news':get_news(), 'user':request.user}
        )


def newspaper(request):
    # like a blog, but for news
    return render_to_response("gmaonewspaper.html",
        {'news':get_news()[:8], 'user':request.user}
        )


def news_view(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    imgs = NewsImg.objects.filter(news=news)
    return render_to_response("gmaonewsview.html",
        {'news':news, 'imgs':imgs, 'user':request.user}
        )


def science(request):
    return render_to_response("gmaoscience.html", 
        {'sciences':get_sciences(), 'user':request.user})


def science_view(request, thing_id):
    science = get_object_or_404(ScienceThing, pk=thing_id)
    video = get_object_or_404(YoutubeVideo, science_thing=science)
    return render_to_response("gmaoscienceview.html", 
        {'science':science, 'video':video, 'user':request.user})


def publications(request):
    return render_to_response("gmaopublications.html", 
        {'publications':get_publications(), 'user':request.user})


def posts(request):
    return render_to_response("gmaoposts.html",
        {'posts':get_posts(), 'user':request.user}
        )


def blog(request):
    # shows 5 more recent, expanded
    return render_to_response("gmaoblog.html",
        {'posts':get_posts()[:5], 'user':request.user}
        )


def post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render_to_response("gmaopostview.html",
        {'post':post, 'user':request.user}
        )


def people(request):
    all_people = People.objects.order_by('name')
    return render_to_response("gmaopeople.html", {'people':all_people, 'user':request.user})


def people_view(request, people_id):
    people = get_object_or_404(People, pk=people_id)
    posts = Post.objects.filter(author=people).order_by('-when')
    publications = Publication.objects.filter(author=people).order_by('-publication_date')
    return render_to_response("gmaopeopleview.html", 
        {'people':people, 'user':request.user, 'posts':posts, 'publications':publications}
        )
    

# RESTRICTED VIEWS SECTION


@login_required
def edit_profile(request):
    user = request.user
    people = get_object_or_404(People, username=user)

    if request.method == 'POST':
        form = FormEditProfile(request.POST, request.FILES, instance=people)
        if form.is_valid():
            form.save()
            return render_to_response("gmaook.html", {'user':user})
    else:
        form = FormEditProfile(instance=people)

    return render_to_response("gmaoeditprofile.html", {'form':form, 'user':user},
                context_instance=RequestContext(request))


@login_required
def edit_configs(request):
    user = request.user
    people = get_object_or_404(People, username=user)

    if request.method == 'POST':
        form = FormPassword(request.POST, request.FILES)
        if form.is_valid():
            curr_passw = form.cleaned_data['current_passw']
            if request.user.check_password(curr_passw):
                new_passw = form.cleaned_data['new_passw']
                request.user.set_password(new_passw)
                request.user.save()
                return render_to_response("gmaook.html", {'user':user})
            else:
                context = RequestContext(request)
                return render_to_response("gmaoeditconfigs.html",
                                          {'form':form, 'user':user, 'erro':True},
                                          context_instance=context)

    else:
        form = FormPassword()

    context = RequestContext(request)
    return render_to_response("gmaoeditconfigs.html", {'form':form, 'user':user},
                              context_instance=context)


@login_required
def create_news(request):
    user = request.user
    people = get_object_or_404(People, username=user)

    if request.method == 'POST':
        form = FormNews(request.POST, request.FILES)
        if form.is_valid():
            news = form.instance
            news.author = people
            news.save()
            return render_to_response("gmaook.html", {'user':user})
        else:
            context = RequestContext(request)
            return render_to_response("gmaocreatenews.html",
                                      {'form':form, 'user':user, 'erro':True},
                                      context_instance=context)

    else:
        form = FormNews()

    context = RequestContext(request)
    return render_to_response("gmaocreatenews.html", {'form':form, 'user':user},
                              context_instance=context)    


@login_required
def create_post(request):
    user = request.user
    people = get_object_or_404(People, username=user)

    if request.method == 'POST':
        form = FormPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.instance
            post.author = people
            post.save()
            return render_to_response("gmaook.html", {'user':user})
        else:
            context = RequestContext(request)
            return render_to_response("gmaocreatepost.html",
                                      {'form':form, 'user':user, 'erro':True},
                                      context_instance=context)

    else:
        form = FormPost()

    context = RequestContext(request)
    return render_to_response("gmaocreatepost.html", {'form':form, 'user':user},
                              context_instance=context)    


@login_required
def create_video(request):
    user = request.user
    people = get_object_or_404(People, username=user)

    if request.method == 'POST':
        form = FormVideo(request.POST, request.FILES)
        if form.is_valid():
            short = form.cleaned_data['short']
            description = form.cleaned_data['description']
            link = form.cleaned_data['youtube_link']
            science = ScienceThing(short=short, description=description)
            science.save()
            video = YoutubeVideo(science_thing=science, video_link=link)
            video.save()
            return render_to_response("gmaook.html", {'user':user})
        else:
            context = RequestContext(request)
            return render_to_response("gmaocreatevideo.html",
                                      {'form':form, 'user':user, 'erro':True},
                                      context_instance=context)

    else:
        form = FormVideo()

    context = RequestContext(request)
    return render_to_response("gmaocreatevideo.html", {'form':form, 'user':user},
                              context_instance=context)    


@login_required
def create_image(request):
    user = request.user

    if request.method == 'POST':
        form = FormImage(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render_to_response("gmaook.html", {'user':user})
        else:
            context = RequestContext(request)
            return render_to_response("gmaocreateimage.html",
                                      {'form':form, 'user':user, 'erro':True},
                                      context_instance=context)

    else:
        form = FormImage()

    context = RequestContext(request)
    return render_to_response("gmaocreateimage.html", {'form':form, 'user':user},
                              context_instance=context)    


@login_required
def upload_publication(request):
    user = request.user
    people = get_object_or_404(People, username=user)

    if request.method == 'POST':
        form = FormPublication(request.POST, request.FILES)
        if form.is_valid():
            pub = form.instance
            pub.author = people
            pub.save()
            return render_to_response("gmaook.html", {'user':user})
        else:
            context = RequestContext(request)
            return render_to_response("gmaouploadpublication.html",
                                      {'form':form, 'user':user, 'erro':True},
                                      context_instance=context)
    else:
        form = FormPublication()

    context = RequestContext(request)
    return render_to_response("gmaouploadpublication.html", {'form':form, 'user':user},
                              context_instance=context)    



# UTILITIES SECTION


def get_imgs_news():
    all_imgs = NewsImg.objects.order_by('-id')[:4]
    imgs = [{'img':img.img, 'caption':img.news.title, 'news':img.news.id} for img in all_imgs]
    return imgs


def get_news(latest=False):
    many_news = News.objects.order_by('-when')[:50]
    if latest:
        many_news = many_news[:4]
    return many_news


def get_sciences(latest=False):
    sciences = ScienceThing.objects.order_by('-id')
    if latest:
        sciences = sciences[:4]
    return sciences


def get_publications(latest=False):
    publications = Publication.objects.order_by('-publication_date')
    if latest:
        publications = publications[:2]
    return publications


def get_posts(latest=False):
    posts = Post.objects.order_by('-when')
    if latest:
        posts = posts[:2]
    return posts
