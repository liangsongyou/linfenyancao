from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import  Artical, Lanmu, Jigou, Suplanmu
from .forms import LanmuForm, ArticalForm


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

# dwebcms管理首页
@login_required
def cms_index(request):
    return render(request, 'dwebcms/index.html')

# dwebcms新建栏目
@login_required
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
@login_required
def cms_listLanmu(request):
    shiju = get_object_or_404(Jigou,name='临汾市局')
    dj_lanmus = Suplanmu.objects.filter(jigou=shiju)

    jigous = Jigou.objects.all()

    context = {
        'dj_lanmus':dj_lanmus,
        'jigous':jigous,
    }
    return render(request, 'dwebcms/listLanmu.html',context)

# dwebcms栏目删除
@login_required
def cms_deleteSubLanmu(request,pk=None):
    item_lanmu = get_object_or_404(Lanmu,pk=pk)
    item_lanmu.delete()
    return redirect('listLanmu')


# dwebcms文章提交
@login_required
def cms_wzTijiao(request,jigou_name=None):
    jigou = get_object_or_404(Jigou,name=jigou_name)
    jigous = Jigou.objects.all()


    if request.method == "POST":
        form = ArticalForm(request.POST,request.FILES)
        if form.is_valid():
            item_biaoti = form.cleaned_data['biaoti']
            item_lanmu_name = form.cleaned_data['lanmu_name']
            item_lanmu = get_object_or_404(Lanmu, name=item_lanmu_name)
            item_file = form.cleaned_data['file']
            item_neirong = form.cleaned_data['neirong']
            item = Artical.objects.create(biaoti=item_biaoti,
                                          neirong=item_neirong,
                                          file=item_file,
                                          lanmu=item_lanmu)
            item.save()
            return redirect(reverse_lazy('wzList'))
    else:
        form = ArticalForm()
    context = {
        'jigou':jigou,
        'form':form,
        'jigous':jigous,

    }
    return render(request,'dwebcms/wzTijiao.html',context)

# dwebcms文章修改
@login_required
def cms_wzXiugai(request,pk):
    artical = Artical.objects.get(pk=pk)
    
    jigous = Jigou.objects.all()
    if request.method == "GET":
        form = ArticalForm()
    if request.method == "POST":
        artical.biaoti = request.POST['biaoti']
        artical.neirong = request.POST['neirong']
        artical.save()
        return redirect(reverse_lazy('wzList'))
    # else:
    #     form = ArticalForm(biaoti=artical.biaoti,
    #                        lanmu_name=artical.lanmu.name,
    #                        file=artical.file,
    #                        neirong=artical.neirong)
    context = {
        'form':form,
        'artical':artical,
        'jigou_name':artical.lanmu.jigou.name,
        'jigou':artical.lanmu.jigou,
    }
    return render(request,'dwebcms/wzXiugai.html',context)

# dwebcms文章列表
@login_required
def cms_wzList(request):
    jigous = Jigou.objects.all()

    q = request.GET.get('q', None)
    jigou_pk = request.GET.get('jigou_pk',None)
    sup_lanmu_pk = request.GET.get('sup_lanmu_pk',None)

    if sup_lanmu_pk is not None and jigou_pk is not "":
        sup_lanmu = Suplanmu.objects.get(pk=int(sup_lanmu_pk))
    else:
        sup_lanmu = None

    artical_list = ''
    jigou = ''

    if q is None or q is "":
        if jigou_pk is None or jigou_pk is "":
            artical_list = Artical.objects.filter(huishou=False)
        else:

            jigou = Jigou.objects.get(pk=int(jigou_pk))
            if jigou.name == "临汾市局":
                if sup_lanmu_pk is not None:
                    sup_lanmu = Suplanmu.objects.get(pk=int(sup_lanmu_pk))

                    artical_list = sup_lanmu.get_all_undelete_articals()
                else:

                    artical_list = jigou.get_all_undelete_articals()
            else:
                artical_list = jigou.get_all_undelete_articals()

    elif q is not None:
        artical_list = Artical.objects.filter(biaoti__contains=q).filter(huishou=False)

    paginator = Paginator(artical_list,5)
    page = request.GET.get('page')
    articals = paginator.get_page(page)

    context = {
        'jigous':jigous,
        'articals':articals,
        'jigou':jigou,
        'sup_lanmu':sup_lanmu,
        'title':'文章列表'
    }
    return render(request,'dwebcms/wzList.html',context)

# dwebcms文章删除
@login_required
def cms_wzDelete(request, pk=None):
    item = get_object_or_404(Artical, pk=pk)
    item.huishou = True
    item.save()
    return redirect(reverse_lazy('wzList'))

# dwebcms文章彻底删除
@login_required
def cms_wzDelete_cd(request, pk=None):
    item = get_object_or_404(Artical, pk=pk)
    item.delete()
    return redirect(reverse_lazy('wzHuishou'))

# dwebcms文章还原
@login_required
def cms_wzHuanyuan(request, pk=None):
    item = get_object_or_404(Artical, pk=pk)
    item.huishou = False
    item.save()
    return redirect(reverse_lazy('wzHuishou'))

# dwebcms文章回收站
@login_required
def cms_wzHuishou(request):
    jigous = Jigou.objects.all()

    q = request.GET.get('q', None)
    jigou_pk = request.GET.get('jigou_pk',None)
    sup_lanmu_pk = request.GET.get('sup_lanmu_pk',None)

    if sup_lanmu_pk is not None and jigou_pk is not "":
        sup_lanmu = Suplanmu.objects.get(pk=int(sup_lanmu_pk))
    else:
        sup_lanmu = None

    artical_list = ''
    jigou = ''

    if q is None or q is "":
        if jigou_pk is None or jigou_pk is "":
            artical_list = Artical.objects.filter(huishou=True)
        else:

            jigou = Jigou.objects.get(pk=int(jigou_pk))
            if jigou.name == "临汾市局":
                if sup_lanmu_pk is not None:
                    sup_lanmu = Suplanmu.objects.get(pk=int(sup_lanmu_pk))

                    artical_list = sup_lanmu.get_all_deleted_articals()
                else:

                    artical_list = jigou.get_all_deleted_articals()
            else:
                artical_list = jigou.get_all_deleted_articals()

    elif q is not None:
        artical_list = Artical.objects.filter(biaoti__contains=q).filter(huishou=True)

    paginator = Paginator(artical_list,5)
    page = request.GET.get('page')
    articals = paginator.get_page(page)

    context = {
        'jigous':jigous,
        'articals':articals,
        'jigou':jigou,
        'sup_lanmu':sup_lanmu,
        'title':'文章回收站'
    }
    return render(request,'dwebcms/wzList.html',context)
