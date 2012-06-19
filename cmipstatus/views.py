from django.shortcuts import render_to_response
from models import Experiment, Member, People, get_tupa_data
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
        run_fraction = 1. / total
        error = (done < 0)
        if error:
            done *= -1
        minfo = {'member':current[1].split('_',1)[-1], 'last':done, 'current':done+1, 'total':total, 'error':error}
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
    editable = request.user == prof.username
    return render_to_response("cmipprofview.html", {'prof':prof, 'editable':editable})


@login_required
def profedit(request, profid):
    return "oi"
