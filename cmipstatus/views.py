from django.shortcuts import render_to_response
from models import Experiment, Member, People, get_tupa_data
from forms import FormEditProfile, FormPassword
from django.template import RequestContext
from os.path import join, exists
from os import listdir
import inpe.settings
from django.http import Http404
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render_to_response("cmiphome.html", {})


@login_required
def explist(request):
    experiments = Experiment.objects.all()
    return render_to_response("cmipexplist.html", {'exps': experiments})

@login_required
def peoplelist(request):
    people = People.objects.all()
    return render_to_response("cmipproflist.html", {'people': people})


@login_required
def expview(request, expname):
    exp = Experiment.objects.get(name=expname)
    members = Member.objects.all().filter(exp=exp)
    exp = [exp]
    tupa_data = get_tupa_data()
    runinfo = []
    info = {'exp':exp}

    if members:
        exp = members

    for member in exp:
        done, total, current = member.get_status(tupa_data)
        finished_prog = float(done) / float(total)
        finished_years = float(done)/12
        total_years = total/12
        run_fraction = 1. / total
        error = (done < 0)
        if error:
            done *= -1
        minfo = {'member':current[1].split('_',1)[-1], 'last':done, 'current':done, 'total':total, 'error':error}
        minfo['complete'] = (done == total)
        minfo['running'] = (current[0] is not None)
        minfo['prog'] = finished_prog
        if minfo['running']:
            minfo['job_id'] = current[0]
            if 'aux' in minfo['job_id']:
                minfo['post'] = True
                minfo['text_run'] = 100
                minfo['prog'] += run_fraction
            else:
                minfo['post'] = False
                minfo['text_run'] = current[-1][:-1]
                minfo['prog'] += float(minfo['text_run'])/100.0 * run_fraction
        minfo['finished_years'] = '%3.2f' % (minfo['prog'] * total_years)
        minfo['total_years'] = total_years
        minfo['text_total'] = "%3.2f" % (minfo['prog']*100)
        runinfo.append(minfo)
        print minfo
    info['title'] = expname
    info['minfo'] = runinfo
    return  render_to_response("cmipexpview.html", info)


@login_required
def expvalview(request, expname):
    #load images for exp
    if '_' not in expname:
        expname += '_1'
    FIGS_DIR = join(inpe.settings.MEDIA_ROOT, 'images', expname, 'figures')
    imgs = []
    if not exists(FIGS_DIR):
        raise Http404
    for uri in listdir(FIGS_DIR):
        imgs.append(join(inpe.settings.MEDIA_URL, 'images', expname, 'figures', uri))
    imgs = zip(imgs[::2], imgs[1::2])
    try:
        logfile = open(join('cmipstatus', 'fetched_data', 'logs', expname+'log.txt'), 'r')
        log = logfile.read()
        logfile.close()
    except:
        log = 'unknown'
    info = {'imgs':imgs, 'expname':expname}
    return render_to_response("cmipexpvalview.html", {'imgs':imgs, 'expname':expname, 'log':log})


@login_required
def profview(request, profid):
    prof = People.objects.get(id=profid)
    user_prof = People.objects.get(username=request.user)
    editable = prof == user_prof
    return render_to_response("cmipprofview.html", {'prof':prof, 'editable':editable})


@login_required
def profedit(request):
    profile = People.objects.get(username=request.user)

    if request.method == 'POST':
        form = FormEditProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render_to_response("cmipsuccess.html", {})
    else:
        form = FormEditProfile(instance=profile)

    return render_to_response("cmipprofedit.html", {'form':form},
                context_instance=RequestContext(request))


@login_required
def passwedit(request):
    if request.method == 'POST':
        profile = People.objects.get(username=request.user)
        form = FormPassword(request.POST, request.FILES)
        if form.is_valid():
            curr_passw = form.cleaned_data['current_passw']
            if request.user.check_password(curr_passw):
                new_passw = form.cleaned_data['new_passw']
                request.user.set_password(new_passw)
                request.user.save()
                return render_to_response("cmipsuccess.html", {})
            else:
                return render_to_response("cmipchangepassw.html", {'form':form, 'erro':True},
                context_instance=RequestContext(request))

    else:
        form = FormPassword()

    return render_to_response("cmipchangepassw.html", {'form':form},
                context_instance=RequestContext(request))
    
