from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from models import Exp, ExpMember
from forms import FormIncludeExp


class Home(View):
    template_name = 'expshome.html'

    def get(self, request):
        user = request.user
        return render(request, self.template_name, {'user':user})


class ExpList(View):
    template_name = 'expslist.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        all_exps = Exp.objects.all()
        return render(request, self.template_name, 
            {'user':user, 
            'running':all_exps,
            'running_errors':[],
            'running_aborted':[],
            'finished':[],
            'finished_aborted':[]})


class ExpView(View):
    template_name = 'expsview.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        exp = Exp.objects.get(id=kwargs['expid'])
        return render(request, self.template_name,
            {'user':user,'exp':exp})


class IncludeNewExp(View):
    template_name = 'expsinclude.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        form = FormIncludeExp()
        return render(request, self.template_name, 
            {'user':user, 'form':form},
            context_instance=RequestContext(request))


    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        form = FormIncludeExp(request.POST, request.FILES)
        if form.is_valid():
            exp = form.instance
            exp.save()
            for i in range(1,form.instance.members + 1):
                new_member = ExpMember(exp=exp, member=i)
                new_member.save()
            return render(request, 'expsok.html', {'user':user})
        return render(request, self.template_name, 
            {'user':user, 'form':form},
            context_instance=RequestContext(request))


