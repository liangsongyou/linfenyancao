from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .models import  Artical, Lanmu, Jigou, Suplanmu
from .forms import LanmuForm


# 市局
def shiju(request):
    return render(request, 'shiju/index.html',{})

# 临烟动态
def dongtai(request,name=None):
    _lanmu = get_object_or_404(Lanmu, name=name)
    articals = Artical.objects.filter(lanmu__name=name)
    context = {
        'articals':articals,
        'lanmu':_lanmu
    }
    return render(request, 'shiju/dongtai.html',context)

# 文章
def artical(request, pk=None):
    item = get_object_or_404(Artical, pk=pk)
    context = {
        'item':item
    }
    return render(request, 'shiju/artical.html', context)

# 领导
def lingdao(request):
    return render(request, 'shiju/lingdao.html', {})

# dwebcms登录
# def cms_login(request):
#     return render(request, 'dwebcms/login.html')

# dwebcms管理首页
def cms_index(request):
    return render(request, 'dwebcms/index.html')

# dwebcms新建栏目
def cms_newLanmu(request):
    jigous = Jigou.objects.all()
    sup_lanmus = Suplanmu.objects.all()
    if request.method == 'POST':
        form = LanmuForm(request.POST)
        if form.is_valid():
            
            item_name = form.cleaned_data['name']

            jigou_name = form.cleaned_data['jigou_name']
            if jigou_name == "":
                item_jigou = None
            else:
                item_jigou = get_object_or_404(Jigou, name=jigou_name)

            sup_lanmu_name = form.cleaned_data['sup_lanmu_name']
            if sup_lanmu_name == "":
                item_sup_lanmu = None
            else:
                item_sup_lanmu = get_object_or_404(Suplanmu, name=sup_lanmu_name)

            item = Lanmu.objects.create(name=item_name, jigou=item_jigou,sup_lanmu=item_sup_lanmu)
            item.save()
            return redirect(reverse_lazy('listLanmu'))
        else:
            error_message=form.errors
    else:
        form = LanmuForm()
    context = {
        'form':form,
        'jigous':jigous,
        'sup_lanmus':sup_lanmus,
        'error_message':form.errors
    }
    return render(request, 'dwebcms/newLanmu.html', context)

# dwebcms栏目列表
def cms_listLanmu(request):
    return render(request, 'dwebcms/listLanmu.html')
