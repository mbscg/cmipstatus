from django import forms
from models import Exp, MemberConfig

class FormIncludeExp(forms.ModelForm):
    class Meta:
        model = Exp


class FormExcludeExp(forms.Form):
    exp = forms.ModelChoiceField(queryset=Exp.objects.all())


class FormMemberConfigs(forms.ModelForm):
    class Meta:
        model = MemberConfig
        exclude = ['member', 'last_gen']
