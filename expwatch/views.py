from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import Exp, ExpMember
from forms import FormIncludeExp

def home(request):
    user = request.user
    return render_to_response("expshome.html", {'user':user})


@login_required
def explist(request):
    user = request.user
    all_exps = Exp.objects.all()
    return render_to_response("expslist.html", 
        {'user':user, 
        'running':all_exps,
        'running_errors':[],
        'running_aborted':[],
        'finished':[],
        'finished_aborted':[]})


@login_required
def expview(request, expid):
    user = request.user
    exp = Exp.objects.get(id=expid)
    return render_to_response("expsview.html",
        {'user':user,'exp':exp})


@login_required
def includenew(request):
    user = request.user
    if request.method == 'POST':
        form = FormIncludeExp(request.POST, request.FILES)
        if form.is_valid():
            exp = form.instance
            exp.save()
            for i in range(1,form.instance.members + 1):
                new_member = ExpMember(exp=exp, member=i)
                new_member.save()
            return render_to_response("expsok.html", {'user':user})
    else:
        form = FormIncludeExp()

    return render_to_response("expsinclude.html", 
        {'user':user, 'form':form},
        context_instance=RequestContext(request))

