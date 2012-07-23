from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from cmipstatus.models import People
import os
from models import News, NewsImg

def home(request):
    return render_to_response("gmaohome.html", 
        {'imgs':get_imgs_news(), 'news':get_latest_news(),
         'user':request.user}
        )

@login_required
def news(request):
    return render_to_response("gmaonews.html",
        {'news':get_lot_of_news(), 'user':request.user}
        )


def news_view(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    return render_to_response("gmaonewsview.html",
        {'news':news, 'user':request.user}
        )

@login_required
def people(request):
    all_people = People.objects.all()
    return render_to_response("gmaopeople.html", {'people':all_people, 'user':request.user})


def get_imgs_news():
    all_imgs = NewsImg.objects.all()
    imgs = [{'img':img.img, 'caption':img.news.title, 'news':img.news.id} for img in all_imgs]
    return imgs


def get_latest_news():
    latest_news = News.objects.order_by('-when')[:6]
    return latest_news


def get_lot_of_news():
    many_news = News.objects.order_by('-when')[:50]
    return many_news
