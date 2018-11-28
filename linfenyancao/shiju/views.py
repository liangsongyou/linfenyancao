from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required



from .models import  Artical, Lanmu, Jigou, Suplanmu, Profile
from .forms import LanmuForm, ArticalForm

FIXED_LANMU_LIST = ['县局动态','县局例会','公示公告','局发文件','通知信息']
FIXED_KESHI_LIST = ['机构职能','工作制度','计划规划','部门动态']


# 市局首页
def shiju(request):
    ldjh = Artical.objects.filter(lanmu__name='领导讲话',huishou=False)[:12]
    ldjh_list = Lanmu.objects.filter(name='领导讲话').first()
    IMGtpxw = Artical.objects.filter(lanmu__name='图片新闻',huishou=False).first()
    IMGlist = Artical.objects.filter(lanmu__name='图片新闻',huishou=False)[:6]
    tpxw_list = Lanmu.objects.filter(name='图片新闻').first()
    lhzh = Artical.objects.filter(lanmu__name='例会专会',huishou=False)[:11]
    lhzh_list = Lanmu.objects.filter(name='例会专会').first()
    jfwj = Artical.objects.filter(lanmu__name='局发文件',huishou=False)[:11]
    jfwj_list = Lanmu.objects.filter(name='局发文件').first()
    tzxx = Artical.objects.filter(lanmu__name='通知信息',huishou=False)[:11]
    tzxx_list = Lanmu.objects.filter(name='通知信息').first()
    hydt = Artical.objects.filter(lanmu__name='行业动态',huishou=False)[:9]
    hydt_list = Lanmu.objects.filter(name='行业动态').first()
    lydt = Artical.objects.filter(lanmu__name='临烟动态',huishou=False)[:9]
    lydt_list = Lanmu.objects.filter(name='临烟动态').first()
    gsgg = Artical.objects.filter(lanmu__name='公示公告',huishou=False)[:20]
    gsgg_list = Lanmu.objects.filter(name='公示公告').first()
    xjdt = Artical.objects.filter(lanmu__name='县局动态',huishou=False)[:10]
    xjdt_list = Lanmu.objects.filter(name='县局动态').first()
    wxyd = Artical.objects.filter(lanmu__name='文学园地',huishou=False)[:11]
    wxyd_list = Lanmu.objects.filter(name='文学园地').first()

    renyuan_list = Profile.objects.all()
    zhiban_list = []
    for item in renyuan_list:
        if item.is_zhiban:
            zhiban_list.append(item)

    linfenshiju = Jigou.objects.get(name='临汾市局')
    xianju_list = Jigou.objects.filter(name__endswith="县")
    keshi_list = []
    jigou_list = Jigou.objects.all()
    for item in jigou_list:
        if item not in xianju_list and item != linfenshiju:
            keshi_list.append(item)


    context = {}
    context['ldjh'] = ldjh
    context['ldjh_list'] = ldjh_list
    context['IMGtpxw'] = IMGtpxw
    context['IMGlist'] = IMGlist
    context['tpxw_list'] = tpxw_list
    context['lhzh'] = lhzh
    context['lhzh_list'] = lhzh_list
    context['jfwj'] = jfwj
    context['jfwj_list'] = jfwj_list
    context['tzxx'] = tzxx
    context['tzxx_list'] = tzxx_list
    context['hydt'] = hydt
    context['hydt_list'] = hydt_list
    context['lydt'] = lydt
    context['lydt_list'] = lydt_list
    context['gsgg'] = gsgg
    context['gsgg_list'] = gsgg_list
    context['xjdt'] = xjdt
    context['xjdt_list'] = xjdt_list
    context['wxyd'] = wxyd
    context['wxyd_list'] = wxyd_list
    context['zhiban_list'] = zhiban_list
    context['xianju_list'] = xianju_list
    context['keshi_list'] = keshi_list
    return render(request, 'shiju/index.html',context)

# 县局
def xianju(request,pk=None):
    item = get_object_or_404(Jigou,pk=pk)

    fixed_lanmu_list = []

    # for name in FIXED_LANMU_LIST:
    #     fixed_lanmu_list.append(Lanmu.objects.get_or_create(name=name,jigou=item)[0])

    for lanmu in item.get_sub_lanmu():
        if lanmu.is_zhiding():
            fixed_lanmu_list.append(lanmu)
    

    context = {}
    context['fixed_lanmu_list'] = fixed_lanmu_list
    context['item'] = item
    return render(request,'shiju/xianju.html',context)

# 科室
def keshi(request,pk=None):
    item = get_object_or_404(Jigou,pk=pk)
    q = request.GET.get('q',None)

    results = ''
    if q is not None and q is not '':
        results = Artical.objects.filter(biaoti__contains=q)

    fixed_keshi_list = []
    for name in FIXED_KESHI_LIST:
        fixed_keshi_list.append(Lanmu.objects.get_or_create(name=name,jigou=item)[0])

    context = {
        'item':item,
        'fixed_keshi_list':fixed_keshi_list,
        'results':results,
    }
    return render(request,'shiju/keshi1.html',context)

# 特殊科室
def teshu_keshi(request):
    context = {}
    return render(request,'shiju/keshi2.html',context)

# 文章列表
def artical_list(request,pk=None):
    lanmu = get_object_or_404(Lanmu, pk=pk)
    articals = Artical.objects.filter(lanmu=lanmu,huishou=False)
    dajia = Artical.objects.filter(huishou=False)[:13]

    page_robot = Paginator(articals, 20)
    page_num = request.GET.get('page')
    try:
        articals = page_robot.page(page_num)
    except EmptyPage:
        articals = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        articals = page_robot.page(1)

    context = {
        'articals':articals,
        'lanmu':lanmu,
        'dajia':dajia
    }
    return render(request, 'shiju/dongtai.html',context)

# 文章
def artical(request, pk=None):
    item = get_object_or_404(Artical, pk=pk)
    next = Artical.objects.filter(lanmu__name=item.lanmu,pk__lt=pk,huishou=False).first()
    pre = Artical.objects.filter(lanmu__name=item.lanmu,
    pk__gt=pk,huishou=False).last()
    context = {
        'item':item,
        'next':next,
        'pre':pre
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

def cms_zhidingSubLanmu(request,pk=None):
    item_lanmu = get_object_or_404(Lanmu,pk=pk)
    if item_lanmu.is_zhiding():
        item_lanmu = False
    else:
        item_lanmu.zhiding = True
    item_lanmu.save()
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

    if sup_lanmu_pk is not None and sup_lanmu_pk is not "":
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
                if sup_lanmu_pk is not None and sup_lanmu_pk is not "":

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
