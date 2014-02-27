from django import forms
from models import Exp

class FormIncludeExp(forms.ModelForm):
    class Meta:
        model = Exp


class FormExcludeExp(forms.Form):
    exp = forms.ModelChoiceField(queryset=Exp.objects.all())
