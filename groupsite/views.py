from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from cmipstatus.models import People
import os
from models import News, NewsImg, ScienceThing, YoutubeVideo
from cmipstatus.forms import FormEditProfile, FormPassword

def home(request):
    return render_to_response("gmaohome.html", 
        {'imgs':get_imgs_news(), 'news':get_news(latest=True),
         'sciences':get_sciences(latest=True), 'user':request.user}
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

def science(request):
    return render_to_response("gmaoscience.html", 
        {'sciences':get_sciences(), 'user':request.user})


def science_view(request, thing_id):
    science = get_object_or_404(ScienceThing, pk=thing_id)
    video = get_object_or_404(YoutubeVideo, science_thing=science)
    return render_to_response("gmaoscienceview.html", 
        {'science':science, 'video':video, 'user':request.user})


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



def people(request):
    all_people = People.objects.all()
    return render_to_response("gmaopeople.html", {'people':all_people, 'user':request.user})


def people_view(request, people_id):
    people = get_object_or_404(People, pk=people_id)
    return render_to_response("gmaopeopleview.html", {'people':people, 'user':request.user})
    

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
    
