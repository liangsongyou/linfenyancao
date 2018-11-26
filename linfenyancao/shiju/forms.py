from django import forms

from .models import Lanmu, Artical

from DjangoUeditor.forms import UEditorField

class LanmuForm(forms.Form):
    name = forms.CharField()
    jigou_name = forms.CharField(required=False)
    sup_lanmu_name = forms.CharField(required=False)


class ArticalForm(forms.Form):
    biaoti = forms.CharField()
    lanmu_name = forms.CharField()
    file = forms.FileField(required=False)
    neirong = UEditorField(u'内容	', width=960, height=500, toolbars="full",
    imagePath="",filePath="",upload_settings={"imageMaxSize":1204000})
