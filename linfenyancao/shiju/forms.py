from django import forms

from .models import Lanmu


class LanmuForm(forms.Form):
    name = forms.CharField()
    jigou_name = forms.CharField(required=False)
    sup_lanmu_name = forms.CharField(required=False)