from django import forms
from models import People

class FormEditProfile(forms.ModelForm):
    class Meta:
        model = People
        fields = ('name', 'about', 'photo')


class FormPassword(forms.Form):
    current_passw = forms.CharField(widget=forms.PasswordInput(render_value=False))
    new_passw = forms.CharField(widget=forms.PasswordInput(render_value=False))    
