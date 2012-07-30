from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404
from cmipstatus.models import People
import os
from models import News, NewsImg, ScienceThing, YoutubeVideo, Post, Publication
from models import NetworkInfo, LattesCache, Editor
from cmipstatus.forms import FormEditProfile, FormPassword
from forms import FormNews, FormPost, FormVideo, FormImage, FormPublication
from forms import FormNetwork
import requests
from requests.exceptions import Timeout
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup
import re
import datetime

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
    all_people = [all_people[i:i+3] for i in range(0, len(all_people), 3)]
    return render_to_response("gmaopeople.html", {'people':all_people, 'user':request.user})


def people_view(request, people_id):
    people = get_object_or_404(People, pk=people_id)
    posts = Post.objects.filter(author=people).order_by('-when').filter(approved=True)
    publications = Publication.objects.filter(author=people).order_by('-publication_date')
    network = NetworkInfo.objects.filter(people=people)
    if network:
        network = network[0]
        lattes_info = get_text_from_lattes_cache(network)
        lattes_pubs = parse_lattes_text(lattes_info)
        social = network.social_icons()
    else:
        lattes_pubs = []
        social = None


    return render_to_response("gmaopeopleview.html", 
        {'people':people, 'user':request.user, 'posts':posts, 'publications':publications,
         'lattes':lattes_pubs, 'social':social}
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
def edit_network(request):
    user = request.user
    people = get_object_or_404(People, username=user)
    network = NetworkInfo.objects.filter(people=people)
    if network:
        network = network[0]
    else:
        network = NetworkInfo(people=people)
        network.save()

    if request.method == 'POST':
        form = FormNetwork(request.POST, request.FILES, instance=network)
        if form.is_valid():
            network = form.instance
            network.people = people
            network.save()
            return render_to_response("gmaook.html", {'user':user})
    else:
        form = FormNetwork(instance=network)

    return render_to_response("gmaoeditnetworking.html", {'form':form, 'user':user},
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


@login_required
def editor_view(request):
    user = request.user
    people = People.objects.get(username=user)
    try:
        editor = get_object_or_404(Editor, people=people)
    except Http404:
        # logged but not editor, sees his queue
        news = News.objects.order_by('-when').filter(approved=False).filter(author=people)
        posts = Post.objects.order_by('-when').filter(approved=False).filter(author=people)
        sciences = ScienceThing.objects.filter(approved=False)
        return render_to_response("gmaopendingposts.html", 
            {'news':news, 'posts':posts, 'sciences':sciences, 'user':user})
    
    # get pending news to approve
    news = News.objects.order_by('-when').filter(approved=False)
    posts = Post.objects.order_by('-when').filter(approved=False)
    sciences = ScienceThing.objects.filter(approved=False)
    return render_to_response("gmaoeditor.html", 
        {'news':news, 'posts':posts, 'sciences':sciences, 'user':user})



@login_required
def auth_post(request, post_id):
    user = request.user
    people = get_object_or_404(People, username=user)
    editor = get_object_or_404(Editor, people=people)
    post = get_object_or_404(Post, pk=post_id)
    post.approved = True
    post.save()
    return render_to_response("gmaook.html", {'user':user})


@login_required
def deny_post(request, post_id):
    user = request.user
    people = get_object_or_404(People, username=user)
    editor = get_object_or_404(Editor, people=people)
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return render_to_response("gmaook.html", {'user':user})


@login_required
def auth_news(request, news_id):
    user = request.user
    people = get_object_or_404(People, username=user)
    editor = get_object_or_404(Editor, people=people)
    news = get_object_or_404(News, pk=news_id)
    news.approved = True
    news.save()
    return render_to_response("gmaook.html", {'user':user})


@login_required
def deny_news(request, news_id):
    user = request.user
    people = get_object_or_404(People, username=user)
    editor = get_object_or_404(Editor, people=people)
    news = get_object_or_404(News, pk=news_id)
    news.delete()
    return render_to_response("gmaook.html", {'user':user})


# UTILITIES SECTION


def get_imgs_news():
    all_imgs = NewsImg.objects.order_by('-id')
    imgs = [{'img':img.img, 'caption':img.news.title, 'news':img.news.id} for img in all_imgs if img.news.approved]
    return imgs


def get_news(latest=False):
    many_news = News.objects.order_by('-when').filter(approved=True)[:50]
    if latest:
        many_news = many_news[:4]
    return many_news


def get_sciences(latest=False):
    sciences = ScienceThing.objects.order_by('-id').filter(approved=True)
    if latest:
        sciences = sciences[:4]
    return sciences


def get_publications(latest=False):
    publications = Publication.objects.order_by('-publication_date')
    if latest:
        publications = publications[:2]
    return publications


def get_posts(latest=False):
    posts = Post.objects.order_by('-when').filter(approved=True)
    if latest:
        posts = posts[:2]
    return posts


def get_text_from_lattes_cache(network):
    # read cache
    try:
        cache = get_object_or_404(LattesCache, people=network.people)
        cache_age = datetime.date.today() - cache.last_update
        if cache_age.days > 5:
            text = get_text_from_lattes(network.lattes)
            cache.text = text
            cache.save()
        return cache.text
    except Http404, e:
        print Http404, e
        text = get_text_from_lattes(network.lattes)
        if text: # no timeout...
            cache = LattesCache(people=network.people, text=text)
            cache.save()
        return cache.text


def get_text_from_lattes(lattes_url):
    validator = URLValidator(verify_exists=False)
    try:
        validator(lattes_url)
        lattes_data = requests.get(lattes_url, timeout=5.000)
    except ValidationError, e:
        print "invalid url", e
        return None
    except Timeout, e:
        print "timeout", e
        return None
    except Exception, e:
        print "unexpected exception", e
        return None
    return lattes_data.text


def parse_lattes_text(text):
    soup = BeautifulSoup(text)
    paper_div = soup.findAll('div', {'class':"artigo-completo"})
    paper_list = []
    year_ptn = re.compile("[0-9]{4}", re.MULTILINE)
    for paper in paper_div:
        paper_line = paper.get_text()
        splitted = paper_line.split(' . ')
        if len(splitted) > 1:
            authors = re.split(year_ptn, splitted[0])
            if len(authors) > 1:
                authors = authors[-1]
            else:
                raise Exception
            publication = splitted[1]
            paper_list.append({'authors':authors, 'publication':publication})
    return paper_list
