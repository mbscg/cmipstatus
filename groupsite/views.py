from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from cmipstatus.models import People
import os
from models import News, NewsImg, ScienceThing, YoutubeVideo

def home(request):
    return render_to_response("gmaohome.html", 
        {'imgs':get_imgs_news(), 'news':get_news(latest=True),
         'science':get_science(latest=True), 'user':request.user}
        )

def news(request):
    return render_to_response("gmaonews.html",
        {'news':get_news(), 'user':request.user}
        )


def news_view(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    return render_to_response("gmaonewsview.html",
        {'news':news, 'user':request.user}
        )

def science_view(request):
    #only videos for now
    return render_to_response("gmaoscience.html", 
        {'video_pairs':get_science(), 'user':request.user})


def people(request):
    all_people = People.objects.all()
    return render_to_response("gmaopeople.html", {'people':all_people, 'user':request.user})


def get_imgs_news():
    all_imgs = NewsImg.objects.order_by('-id')[:4]
    imgs = [{'img':img.img, 'caption':img.news.title, 'news':img.news.id} for img in all_imgs]
    return imgs


def get_news(latest=False):
    many_news = News.objects.order_by('-when')[:50]
    if latest:
        many_news = many_news[:4]
    return many_news


def get_science(latest=False):
    all_videos = YoutubeVideo.objects.order_by('-id')
    video_pairs = [[video, video.science_thing] for video in all_videos]
    if latest:
        video_pairs = video_pairs[:4]
    return video_pairs
    
