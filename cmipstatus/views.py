from django.shortcuts import render_to_response
from models import Experiment, TupaQuery, Member, get_tupa_data
from os.path import join, exists
import inpe.settings
from django.http import Http404

def home(request):
    return render_to_response("cmiphome.html", {})


def explist(request):
    experiments = Experiment.objects.all()
    return render_to_response("cmipexplist.html", {'exps': experiments})


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
        minfo = {'member':current[1].split('_',1)[-1], 'current':done+1, 'total':total}
        if current[0] == None: #not running
            minfo['running'] = False
            minfo['prog'] = 0.0 * run_fraction + finished_prog
            minfo['text_run'] = '0'
            minfo['text_total'] = "%3.2f" % (minfo['prog']*100)
        else:
            minfo['running'] = True
            minfo['job_id'] = current[0]
            if 'aux' in current[0]:
                minfo['post'] = True
                minfo['text_run'] = '100'
                minfo['prog'] = 1.0 * run_fraction + finished_prog
                minfo['text_total'] = "%3.2f" % (minfo['prog']*100)
            else:
                minfo['post'] = False
                minfo['text_run'] = current[-1][:-1]
                minfo['prog'] = float(minfo['text_run'])/100.0 * run_fraction + finished_prog
                minfo['text_total'] = "%3.2f" % (minfo['prog']*100)
        runinfo.append(minfo)

    info['minfo'] = runinfo
    return  render_to_response("cmipexpview.html", info)


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
    info = {'imgs':imgs, 'expname':expname}
    return render_to_response("cmipexpvalview.html", {'imgs':imgs, 'expname':expname})
